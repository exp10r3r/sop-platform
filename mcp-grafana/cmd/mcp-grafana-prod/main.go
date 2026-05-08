// mcp-grafana-prod 是 mcp-grafana 的定制版本，内置 CAS (银盛统一认证) 支持。
// 启动时交互式输入 LDAP 用户名密码，自动获取并维护 CAS JWT，
// 在所有 Grafana API 请求中注入 office_to_prod_token Cookie 绕过 openresty CAS 拦截。
package main

import (
	"context"
	"crypto/tls"
	"encoding/base64"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"io"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"slices"
	"strings"
	"sync"
	"syscall"
	"time"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
	"golang.org/x/term"

	mcpgrafana "github.com/grafana/mcp-grafana"
	"github.com/grafana/mcp-grafana/observability"
	"github.com/grafana/mcp-grafana/tools"
)

const (
	casBaseURL = "https://cas.eptok.com"
	casLoginPath = "/api/base-user/auth/ad/"
	casRefreshPath = "/api/base-user/auth/refresh/"
	casCookieName = "office_to_prod_token"
	tokenRefreshMargin = 120 * time.Second
)

// CASAuth 管理 CAS JWT 的获取和自动刷新
type CASAuth struct {
	username     string
	password     string
	jwt          string
	refreshToken string
	expireTime   time.Time
	mu           sync.RWMutex
	httpClient   *http.Client
}

type casLoginResponse struct {
	RetCode string `json:"retcode"`
	RetMsg  string `json:"retmsg"`
	Data    struct {
		JWTToken     string `json:"jwt_token"`
		RefreshToken string `json:"refresh_token"`
	} `json:"data"`
}

func NewCASAuth(username, password string) (*CASAuth, error) {
	ca := &CASAuth{
		username: username,
		password: password,
		httpClient: &http.Client{
			Timeout: 10 * time.Second,
			Transport: &http.Transport{
				TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
			},
		},
	}
	if err := ca.login(); err != nil {
		return nil, err
	}
	return ca, nil
}

func (ca *CASAuth) login() error {
	payload, _ := json.Marshal(map[string]string{
		"username": ca.username,
		"password": ca.password,
	})

	req, err := http.NewRequest("POST", casBaseURL+casLoginPath, strings.NewReader(string(payload)))
	if err != nil {
		return fmt.Errorf("创建登录请求失败: %w", err)
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := ca.httpClient.Do(req)
	if err != nil {
		return fmt.Errorf("CAS 登录请求失败: %w", err)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	var result casLoginResponse
	if err := json.Unmarshal(body, &result); err != nil {
		return fmt.Errorf("解析登录响应失败: %w", err)
	}
	if result.RetCode != "0000" {
		return fmt.Errorf("CAS 登录失败: %s - %s", result.RetCode, result.RetMsg)
	}

	ca.jwt = result.Data.JWTToken
	ca.refreshToken = result.Data.RefreshToken
	ca.expireTime = parseJWTExpiry(ca.jwt)

	slog.Info("CAS 登录成功", "expire", ca.expireTime.Format("15:04:05"))
	return nil
}

func (ca *CASAuth) refresh() error {
	if ca.refreshToken == "" {
		return ca.login()
	}

	payload, _ := json.Marshal(map[string]string{
		"refresh_token": ca.refreshToken,
	})

	req, err := http.NewRequest("POST", casBaseURL+casRefreshPath, strings.NewReader(string(payload)))
	if err != nil {
		return ca.login()
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := ca.httpClient.Do(req)
	if err != nil {
		slog.Warn("Token 刷新请求失败，尝试重新登录", "error", err)
		return ca.login()
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	var result casLoginResponse
	if err := json.Unmarshal(body, &result); err != nil || result.RetCode != "0000" {
		slog.Warn("Token 刷新失败，尝试重新登录")
		return ca.login()
	}

	ca.jwt = result.Data.JWTToken
	if result.Data.RefreshToken != "" {
		ca.refreshToken = result.Data.RefreshToken
	}
	ca.expireTime = parseJWTExpiry(ca.jwt)

	slog.Info("CAS Token 刷新成功", "expire", ca.expireTime.Format("15:04:05"))
	return nil
}

// Token 返回有效的 JWT，过期前自动刷新
func (ca *CASAuth) Token() string {
	ca.mu.RLock()
	if time.Now().Before(ca.expireTime.Add(-tokenRefreshMargin)) {
		token := ca.jwt
		ca.mu.RUnlock()
		return token
	}
	ca.mu.RUnlock()

	ca.mu.Lock()
	defer ca.mu.Unlock()
	// double check
	if time.Now().Before(ca.expireTime.Add(-tokenRefreshMargin)) {
		return ca.jwt
	}
	if err := ca.refresh(); err != nil {
		slog.Error("CAS Token 刷新失败", "error", err)
	}
	return ca.jwt
}

func parseJWTExpiry(token string) time.Time {
	parts := strings.Split(token, ".")
	if len(parts) != 3 {
		return time.Now().Add(10 * time.Minute)
	}
	payload := parts[1]
	// base64 padding
	switch len(payload) % 4 {
	case 2:
		payload += "=="
	case 3:
		payload += "="
	}
	decoded, err := base64.URLEncoding.DecodeString(payload)
	if err != nil {
		decoded, err = base64.RawURLEncoding.DecodeString(parts[1])
		if err != nil {
			return time.Now().Add(10 * time.Minute)
		}
	}
	var claims struct {
		Exp float64 `json:"exp"`
	}
	if err := json.Unmarshal(decoded, &claims); err != nil || claims.Exp == 0 {
		return time.Now().Add(10 * time.Minute)
	}
	return time.Unix(int64(claims.Exp), 0)
}

// CASRoundTripper 在每个请求中注入 office_to_prod_token Cookie
type CASRoundTripper struct {
	underlying http.RoundTripper
	casAuth    *CASAuth
}

func (rt *CASRoundTripper) RoundTrip(req *http.Request) (*http.Response, error) {
	clonedReq := req.Clone(req.Context())

	token := rt.casAuth.Token()
	if existing := clonedReq.Header.Get("Cookie"); existing != "" {
		clonedReq.Header.Set("Cookie", existing+"; "+casCookieName+"="+token)
	} else {
		clonedReq.Header.Set("Cookie", casCookieName+"="+token)
	}

	return rt.underlying.RoundTrip(clonedReq)
}

// --- 以下是从原版 main.go 复制并适配的代码 ---

func maybeAddTools(s *server.MCPServer, tf func(*server.MCPServer), enabledTools []string, disable bool, category string) {
	if !slices.Contains(enabledTools, category) {
		return
	}
	if disable {
		return
	}
	tf(s)
}

type disabledTools struct {
	enabledTools string
	search, datasource, incident,
	prometheus, loki, elasticsearch, influxdb, alerting,
	dashboard, folder, oncall, asserts, sift, admin,
	pyroscope, navigation, proxied, annotations, rendering, cloudwatch, write,
	examples, clickhouse, searchlogs, graphite,
	runpanelquery bool
}

type grafanaConfig struct {
	debug           bool
	tlsCertFile     string
	tlsKeyFile      string
	tlsCAFile       string
	tlsSkipVerify   bool
	maxLokiLogLimit int
}

func (dt *disabledTools) addFlags() {
	flag.StringVar(&dt.enabledTools, "enabled-tools", "search,datasource,incident,prometheus,loki,alerting,dashboard,folder,oncall,asserts,sift,pyroscope,navigation,proxied,annotations,rendering", "Comma separated list of enabled tools")
	flag.BoolVar(&dt.search, "disable-search", false, "Disable search tools")
	flag.BoolVar(&dt.datasource, "disable-datasource", false, "Disable datasource tools")
	flag.BoolVar(&dt.incident, "disable-incident", false, "Disable incident tools")
	flag.BoolVar(&dt.prometheus, "disable-prometheus", false, "Disable prometheus tools")
	flag.BoolVar(&dt.loki, "disable-loki", false, "Disable loki tools")
	flag.BoolVar(&dt.elasticsearch, "disable-elasticsearch", false, "Disable elasticsearch tools")
	flag.BoolVar(&dt.influxdb, "disable-influxdb", false, "Disable InfluxDB tools")
	flag.BoolVar(&dt.alerting, "disable-alerting", false, "Disable alerting tools")
	flag.BoolVar(&dt.dashboard, "disable-dashboard", false, "Disable dashboard tools")
	flag.BoolVar(&dt.folder, "disable-folder", false, "Disable folder tools")
	flag.BoolVar(&dt.oncall, "disable-oncall", false, "Disable oncall tools")
	flag.BoolVar(&dt.asserts, "disable-asserts", false, "Disable asserts tools")
	flag.BoolVar(&dt.sift, "disable-sift", false, "Disable sift tools")
	flag.BoolVar(&dt.admin, "disable-admin", false, "Disable admin tools")
	flag.BoolVar(&dt.pyroscope, "disable-pyroscope", false, "Disable pyroscope tools")
	flag.BoolVar(&dt.navigation, "disable-navigation", false, "Disable navigation tools")
	flag.BoolVar(&dt.proxied, "disable-proxied", false, "Disable proxied tools")
	flag.BoolVar(&dt.write, "disable-write", false, "Disable write tools")
	flag.BoolVar(&dt.annotations, "disable-annotations", false, "Disable annotation tools")
	flag.BoolVar(&dt.rendering, "disable-rendering", false, "Disable rendering tools")
	flag.BoolVar(&dt.cloudwatch, "disable-cloudwatch", false, "Disable CloudWatch tools")
	flag.BoolVar(&dt.examples, "disable-examples", false, "Disable query examples tools")
	flag.BoolVar(&dt.clickhouse, "disable-clickhouse", false, "Disable ClickHouse tools")
	flag.BoolVar(&dt.searchlogs, "disable-searchlogs", false, "Disable search logs tools")
	flag.BoolVar(&dt.runpanelquery, "disable-runpanelquery", false, "Disable run panel query tools")
	flag.BoolVar(&dt.graphite, "disable-graphite", false, "Disable Graphite tools")
}

func (gc *grafanaConfig) addFlags() {
	flag.BoolVar(&gc.debug, "debug", false, "Enable debug mode")
	flag.StringVar(&gc.tlsCertFile, "tls-cert-file", "", "TLS certificate file")
	flag.StringVar(&gc.tlsKeyFile, "tls-key-file", "", "TLS private key file")
	flag.StringVar(&gc.tlsCAFile, "tls-ca-file", "", "TLS CA certificate file")
	flag.BoolVar(&gc.tlsSkipVerify, "tls-skip-verify", false, "Skip TLS verification")
	flag.IntVar(&gc.maxLokiLogLimit, "max-loki-log-limit", tools.MaxLokiLogLimit, "Max Loki log lines per query")
}

func (dt *disabledTools) addTools(s *server.MCPServer) {
	enabledTools := strings.Split(dt.enabledTools, ",")
	enableWriteTools := !dt.write
	maybeAddTools(s, tools.AddSearchTools, enabledTools, dt.search, "search")
	maybeAddTools(s, tools.AddDatasourceTools, enabledTools, dt.datasource, "datasource")
	maybeAddTools(s, func(m *server.MCPServer) { tools.AddIncidentTools(m, enableWriteTools) }, enabledTools, dt.incident, "incident")
	maybeAddTools(s, tools.AddPrometheusTools, enabledTools, dt.prometheus, "prometheus")
	maybeAddTools(s, tools.AddLokiTools, enabledTools, dt.loki, "loki")
	maybeAddTools(s, tools.AddElasticsearchTools, enabledTools, dt.elasticsearch, "elasticsearch")
	maybeAddTools(s, tools.AddInfluxDBTools, enabledTools, dt.influxdb, "influxdb")
	maybeAddTools(s, func(m *server.MCPServer) { tools.AddAlertingTools(m, enableWriteTools) }, enabledTools, dt.alerting, "alerting")
	maybeAddTools(s, func(m *server.MCPServer) { tools.AddDashboardTools(m, enableWriteTools) }, enabledTools, dt.dashboard, "dashboard")
	maybeAddTools(s, func(m *server.MCPServer) { tools.AddFolderTools(m, enableWriteTools) }, enabledTools, dt.folder, "folder")
	maybeAddTools(s, tools.AddOnCallTools, enabledTools, dt.oncall, "oncall")
	maybeAddTools(s, tools.AddAssertsTools, enabledTools, dt.asserts, "asserts")
	maybeAddTools(s, func(m *server.MCPServer) { tools.AddSiftTools(m, enableWriteTools) }, enabledTools, dt.sift, "sift")
	maybeAddTools(s, tools.AddAdminTools, enabledTools, dt.admin, "admin")
	maybeAddTools(s, tools.AddPyroscopeTools, enabledTools, dt.pyroscope, "pyroscope")
	maybeAddTools(s, tools.AddNavigationTools, enabledTools, dt.navigation, "navigation")
	maybeAddTools(s, func(m *server.MCPServer) { tools.AddAnnotationTools(m, enableWriteTools) }, enabledTools, dt.annotations, "annotations")
	maybeAddTools(s, tools.AddRenderingTools, enabledTools, dt.rendering, "rendering")
	maybeAddTools(s, tools.AddCloudWatchTools, enabledTools, dt.cloudwatch, "cloudwatch")
	maybeAddTools(s, tools.AddExamplesTools, enabledTools, dt.examples, "examples")
	maybeAddTools(s, tools.AddClickHouseTools, enabledTools, dt.clickhouse, "clickhouse")
	maybeAddTools(s, tools.AddSearchLogsTools, enabledTools, dt.searchlogs, "searchlogs")
	maybeAddTools(s, tools.AddRunPanelQueryTools, enabledTools, dt.runpanelquery, "runpanelquery")
	maybeAddTools(s, tools.AddGraphiteTools, enabledTools, dt.graphite, "graphite")
}

func newServer(dt disabledTools, obs *observability.Observability) (*server.MCPServer, *mcpgrafana.ToolManager, *mcpgrafana.SessionManager) {
	sm := mcpgrafana.NewSessionManager(
		mcpgrafana.WithSessionTTL(30 * time.Minute),
	)

	var stm *mcpgrafana.ToolManager
	var s *server.MCPServer

	hooks := &server.Hooks{
		OnRegisterSession:   []server.OnRegisterSessionHookFunc{sm.CreateSession},
		OnUnregisterSession: []server.OnUnregisterSessionHookFunc{sm.RemoveSession},
	}

	hooks = observability.MergeHooks(hooks, obs.MCPHooks())

	s = server.NewMCPServer("mcp-grafana-prod", mcpgrafana.Version(),
		server.WithInstructions(`This server provides access to your Grafana production instance (behind CAS SSO).
CAS authentication is handled automatically - no proxy needed.`),
		server.WithHooks(hooks),
	)

	stm = mcpgrafana.NewToolManager(sm, s, mcpgrafana.WithProxiedTools(!dt.proxied))
	sm.SetMCPServer(s)
	dt.addTools(s)
	return s, stm, sm
}

func readPassword() (string, error) {
	fd := int(os.Stdin.Fd())
	if term.IsTerminal(fd) {
		pw, err := term.ReadPassword(fd)
		return string(pw), err
	}
	// 如果 stdin 不是终端（如管道），从环境变量读取
	pw := os.Getenv("CAS_PASSWORD")
	if pw != "" {
		return pw, nil
	}
	return "", fmt.Errorf("非终端模式下请设置 CAS_PASSWORD 环境变量")
}

func main() {
	var dt disabledTools
	dt.addFlags()
	var gc grafanaConfig
	gc.addFlags()
	logLevel := flag.String("log-level", "info", "Log level")
	showVersion := flag.Bool("version", false, "Print version and exit")
	var obs observability.Config
	flag.Parse()

	if *showVersion {
		fmt.Println(mcpgrafana.Version())
		os.Exit(0)
	}

	var l slog.Level
	_ = l.UnmarshalText([]byte(*logLevel))
	slog.SetDefault(slog.New(slog.NewTextHandler(os.Stderr, &slog.HandlerOptions{Level: l})))

	// 交互式输入 CAS 凭据
	username := os.Getenv("CAS_USERNAME")
	if username == "" {
		fmt.Fprint(os.Stderr, "请输入 CAS/LDAP 用户名: ")
		fmt.Scanln(&username)
	}
	if username == "" {
		fmt.Fprintln(os.Stderr, "用户名不能为空")
		os.Exit(1)
	}

	password := os.Getenv("CAS_PASSWORD")
	if password == "" {
		fmt.Fprint(os.Stderr, "请输入 CAS/LDAP 密码: ")
		var err error
		password, err = readPassword()
		fmt.Fprintln(os.Stderr) // 换行
		if err != nil {
			fmt.Fprintf(os.Stderr, "读取密码失败: %v\n", err)
			os.Exit(1)
		}
	}

	// 初始化 CAS 认证
	casAuth, err := NewCASAuth(username, password)
	if err != nil {
		fmt.Fprintf(os.Stderr, "CAS 认证失败: %v\n", err)
		os.Exit(1)
	}

	// 构建带 CAS Cookie 注入的 BaseTransport
	baseTransport := &CASRoundTripper{
		underlying: &http.Transport{
			TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
			Proxy:           http.ProxyFromEnvironment,
		},
		casAuth: casAuth,
	}

	grafanaCfg := mcpgrafana.GrafanaConfig{
		Debug:           gc.debug,
		MaxLokiLogLimit: gc.maxLokiLogLimit,
		BaseTransport:   baseTransport,
	}
	if gc.tlsCertFile != "" || gc.tlsKeyFile != "" || gc.tlsCAFile != "" || gc.tlsSkipVerify {
		grafanaCfg.TLSConfig = &mcpgrafana.TLSConfig{
			CertFile:   gc.tlsCertFile,
			KeyFile:    gc.tlsKeyFile,
			CAFile:     gc.tlsCAFile,
			SkipVerify: gc.tlsSkipVerify,
		}
	}

	obs.ServerName = "mcp-grafana-prod"
	obs.ServerVersion = mcpgrafana.Version()

	o, err := observability.Setup(obs)
	if err != nil {
		panic(fmt.Errorf("observability setup failed: %w", err))
	}
	defer func() {
		shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		_ = o.Shutdown(shutdownCtx)
	}()

	s, tm, sm := newServer(dt, o)
	defer sm.Close()

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-sigChan
		slog.Info("收到关闭信号")
		cancel()
		_ = os.Stdin.Close()
	}()

	// stdio 模式
	srv := server.NewStdioServer(s)
	cf := mcpgrafana.ComposedStdioContextFunc(grafanaCfg)
	srv.SetContextFunc(cf)

	if !dt.proxied {
		stdioCtx := cf(ctx)
		if err := tm.InitializeAndRegisterServerTools(stdioCtx); err != nil {
			slog.Error("初始化 proxied tools 失败", "error", err)
		}
	}

	slog.Info("mcp-grafana-prod 启动", "version", mcpgrafana.Version())

	if err := srv.Listen(ctx, os.Stdin, os.Stdout); err != nil && !errors.Is(err, context.Canceled) {
		panic(fmt.Errorf("server error: %v", err))
	}
}

// 确保编译时检查接口
var _ http.RoundTripper = (*CASRoundTripper)(nil)
var _ mcp.MCPMethod = mcp.MCPMethod("") // 确保 mcp 包被使用
