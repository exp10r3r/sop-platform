"""认证API"""

from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, AuditLog
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    create_user,
    log_audit,
    hash_password,
    verify_password
)
from app.utils.auth import get_current_user, get_admin_user

router = APIRouter(prefix="/auth", tags=["认证"])


# 请求模型
class LoginRequest(BaseModel):
    username: str
    password: str
    remember: bool = False


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


# 响应模型
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    last_login: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/login", summary="用户登录")
async def login(
    request: Request,
    data: LoginRequest,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """用户登录"""
    user = authenticate_user(db, data.username, data.password)

    if not user:
        # 记录登录失败日志
        log_audit(
            db=db,
            action="login_failed",
            details=f"尝试登录用户: {data.username}",
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 更新最后登录时间
    user.last_login = datetime.now()
    db.commit()

    # 生成Token
    token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )

    # 记录登录日志
    log_audit(
        db=db,
        user_id=user.id,
        action="login",
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    return {
        "status": True,
        "data": {
            "token": token,
            "user": UserResponse.model_validate(user).model_dump()
        }
    }


@router.post("/logout", summary="用户登出")
async def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """用户登出"""
    # 记录登出日志
    log_audit(
        db=db,
        user_id=current_user.id,
        action="logout",
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    return {"status": True, "message": "登出成功"}


@router.post("/register", summary="创建用户（仅管理员）")
async def register(
    request: Request,
    data: RegisterRequest,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """创建新用户（仅管理员可操作）"""
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )

    # 检查邮箱是否已存在
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已存在"
        )

    # 验证角色
    if data.role not in ["admin", "user"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的角色"
        )

    # 创建用户
    user = create_user(
        db=db,
        username=data.username,
        email=data.email,
        password=data.password,
        role=data.role
    )

    # 记录审计日志
    log_audit(
        db=db,
        user_id=current_user.id,
        action="create",
        resource="user",
        resource_id=user.id,
        details=f"创建用户: {user.username}",
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    return {
        "status": True,
        "message": "用户创建成功",
        "data": UserResponse.model_validate(user).model_dump()
    }


@router.get("/me", summary="获取当前用户信息")
async def get_me(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """获取当前登录用户信息"""
    return {
        "status": True,
        "data": UserResponse.model_validate(current_user).model_dump()
    }


@router.put("/password", summary="修改密码")
async def change_password(
    request: Request,
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """修改密码"""
    # 验证旧密码
    if not verify_password(data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="旧密码错误"
        )

    # 更新密码
    current_user.password_hash = hash_password(data.new_password)
    db.commit()

    # 记录审计日志
    log_audit(
        db=db,
        user_id=current_user.id,
        action="update",
        resource="password",
        details="修改密码",
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    return {"status": True, "message": "密码修改成功"}


@router.get("/users", summary="用户列表（仅管理员）")
async def list_users(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取用户列表（仅管理员）"""
    users = db.query(User).all()
    return {
        "status": True,
        "data": [UserResponse.model_validate(u).model_dump() for u in users]
    }


@router.delete("/users/{user_id}", summary="删除用户（仅管理员）")
async def delete_user(
    user_id: int,
    request: Request,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """删除用户（仅管理员）"""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除自己"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 记录审计日志
    log_audit(
        db=db,
        user_id=current_user.id,
        action="delete",
        resource="user",
        resource_id=user.id,
        details=f"删除用户: {user.username}",
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )

    db.delete(user)
    db.commit()

    return {"status": True, "message": "用户已删除"}


@router.get("/audit-logs", summary="审计日志列表（仅管理员）")
async def list_audit_logs(
    page: int = 1,
    page_size: int = 20,
    action: Optional[str] = None,
    user_id: Optional[int] = None,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """获取审计日志列表（仅管理员）"""
    query = db.query(AuditLog)

    if action:
        query = query.filter(AuditLog.action == action)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)

    total = query.count()
    logs = query.order_by(AuditLog.created_at.desc()).offset(
        (page - 1) * page_size
    ).limit(page_size).all()

    return {
        "status": True,
        "data": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": [
                {
                    "id": log.id,
                    "user_id": log.user_id,
                    "action": log.action,
                    "resource": log.resource,
                    "resource_id": log.resource_id,
                    "details": log.details,
                    "ip_address": log.ip_address,
                    "created_at": log.created_at.isoformat() if log.created_at else None
                }
                for log in logs
            ]
        }
    }