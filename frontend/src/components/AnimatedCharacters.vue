<template>
  <div class="animated-characters" ref="containerRef">
    <!-- Purple tall rectangle character - Back layer -->
    <div
      ref="purpleRef"
      class="character purple"
      :style="purpleStyle"
    >
      <div class="eyes" :style="purpleEyesStyle">
        <EyeBall
          :size="18"
          :pupilSize="7"
          :maxDistance="5"
          :isBlinking="isPurpleBlinking"
          :forceLookX="purpleForceLookX"
          :forceLookY="purpleForceLookY"
        />
        <EyeBall
          :size="18"
          :pupilSize="7"
          :maxDistance="5"
          :isBlinking="isPurpleBlinking"
          :forceLookX="purpleForceLookX"
          :forceLookY="purpleForceLookY"
        />
      </div>
    </div>

    <!-- Black tall rectangle character - Middle layer -->
    <div
      ref="blackRef"
      class="character black"
      :style="blackStyle"
    >
      <div class="eyes" :style="blackEyesStyle">
        <EyeBall
          :size="16"
          :pupilSize="6"
          :maxDistance="4"
          :isBlinking="isBlackBlinking"
          :forceLookX="blackForceLookX"
          :forceLookY="blackForceLookY"
        />
        <EyeBall
          :size="16"
          :pupilSize="6"
          :maxDistance="4"
          :isBlinking="isBlackBlinking"
          :forceLookX="blackForceLookX"
          :forceLookY="blackForceLookY"
        />
      </div>
    </div>

    <!-- Orange semi-circle character - Front left -->
    <div
      ref="orangeRef"
      class="character orange"
      :style="orangeStyle"
    >
      <div class="eyes pupils-only" :style="orangeEyesStyle">
        <Pupil :size="12" :maxDistance="5" :forceLookX="orangeForceLookX" :forceLookY="orangeForceLookY" />
        <Pupil :size="12" :maxDistance="5" :forceLookX="orangeForceLookX" :forceLookY="orangeForceLookY" />
      </div>
    </div>

    <!-- Yellow tall rectangle character - Front right -->
    <div
      ref="yellowRef"
      class="character yellow"
      :style="yellowStyle"
    >
      <div class="eyes pupils-only" :style="yellowEyesStyle">
        <Pupil :size="12" :maxDistance="5" :forceLookX="yellowForceLookX" :forceLookY="yellowForceLookY" />
        <Pupil :size="12" :maxDistance="5" :forceLookX="yellowForceLookX" :forceLookY="yellowForceLookY" />
      </div>
      <div class="mouth" :style="yellowMouthStyle"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import EyeBall from './EyeBall.vue'
import Pupil from './Pupil.vue'

const props = defineProps({
  isTyping: {
    type: Boolean,
    default: false
  },
  showPassword: {
    type: Boolean,
    default: false
  },
  passwordLength: {
    type: Number,
    default: 0
  }
})

const containerRef = ref(null)
const purpleRef = ref(null)
const blackRef = ref(null)
const orangeRef = ref(null)
const yellowRef = ref(null)

const mouseX = ref(0)
const mouseY = ref(0)
const isPurpleBlinking = ref(false)
const isBlackBlinking = ref(false)
const isLookingAtEachOther = ref(false)
const isPurplePeeking = ref(false)

// Mouse move handler
const handleMouseMove = (e) => {
  mouseX.value = e.clientX
  mouseY.value = e.clientY
}

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove)
})

onUnmounted(() => {
  window.removeEventListener('mousemove', handleMouseMove)
})

// Blinking effect for purple character
let purpleBlinkTimeout = null
const schedulePurpleBlink = () => {
  const randomInterval = Math.random() * 4000 + 3000
  purpleBlinkTimeout = setTimeout(() => {
    isPurpleBlinking.value = true
    setTimeout(() => {
      isPurpleBlinking.value = false
      schedulePurpleBlink()
    }, 150)
  }, randomInterval)
}

// Blinking effect for black character
let blackBlinkTimeout = null
const scheduleBlackBlink = () => {
  const randomInterval = Math.random() * 4000 + 3000
  blackBlinkTimeout = setTimeout(() => {
    isBlackBlinking.value = true
    setTimeout(() => {
      isBlackBlinking.value = false
      scheduleBlackBlink()
    }, 150)
  }, randomInterval)
}

onMounted(() => {
  schedulePurpleBlink()
  scheduleBlackBlink()
})

onUnmounted(() => {
  if (purpleBlinkTimeout) clearTimeout(purpleBlinkTimeout)
  if (blackBlinkTimeout) clearTimeout(blackBlinkTimeout)
})

// Looking at each other when typing
watch(() => props.isTyping, (newVal) => {
  if (newVal) {
    isLookingAtEachOther.value = true
    setTimeout(() => {
      isLookingAtEachOther.value = false
    }, 800)
  } else {
    isLookingAtEachOther.value = false
  }
})

// Purple sneaky peeking - 只在显示密码时触发（原项目逻辑）
let purplePeekTimeout = null
watch([() => props.passwordLength, () => props.showPassword], () => {
  // 当密码显示时，紫色角色会偶尔偷看
  if (props.passwordLength > 0 && props.showPassword) {
    const schedulePeek = () => {
      const peekInterval = setTimeout(() => {
        isPurplePeeking.value = true
        setTimeout(() => {
          isPurplePeeking.value = false
        }, 800)
      }, Math.random() * 3000 + 2000)
      return peekInterval
    }
    purplePeekTimeout = schedulePeek()
  } else {
    isPurplePeeking.value = false
  }
}, { immediate: true })

// Calculate position helper
const calculatePosition = (refValue) => {
  if (!refValue) return { faceX: 0, faceY: 0, bodySkew: 0 }

  const rect = refValue.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 3

  const deltaX = mouseX.value - centerX
  const deltaY = mouseY.value - centerY

  const faceX = Math.max(-15, Math.min(15, deltaX / 20))
  const faceY = Math.max(-10, Math.min(10, deltaY / 30))
  const bodySkew = Math.max(-6, Math.min(6, -deltaX / 120))

  return { faceX, faceY, bodySkew }
}

// 完全按照原项目逻辑
const isHidingPassword = computed(() => props.passwordLength > 0 && !props.showPassword)
const isShowingPassword = computed(() => props.passwordLength > 0 && props.showPassword)

// Purple character styles
const purplePos = computed(() => calculatePosition(purpleRef.value))
const purpleStyle = computed(() => ({
  left: '70px',
  width: '180px',
  height: (props.isTyping || isHidingPassword.value) ? '440px' : '400px',
  transform: isShowingPassword.value
    ? 'skewX(0deg)'  // 显示密码时，身体正常（背过去）
    : (props.isTyping || isHidingPassword.value)
      ? `skewX(${purplePos.value.bodySkew - 12}deg) translateX(40px)` // 隐藏密码时，身体倾斜遮挡
      : `skewX(${purplePos.value.bodySkew}deg)`
}))
const purpleEyesStyle = computed(() => ({
  left: isShowingPassword.value ? '20px' : isLookingAtEachOther.value ? '55px' : `${45 + purplePos.value.faceX}px`,
  top: isShowingPassword.value ? '35px' : isLookingAtEachOther.value ? '65px' : `${40 + purplePos.value.faceY}px`
}))
const purpleForceLookX = computed(() => {
  if (isShowingPassword.value) return isPurplePeeking.value ? 4 : -4  // 显示密码时偷看
  if (isLookingAtEachOther.value) return 3
  return undefined
})
const purpleForceLookY = computed(() => {
  if (isShowingPassword.value) return isPurplePeeking.value ? 5 : -4
  if (isLookingAtEachOther.value) return 4
  return undefined
})

// Black character styles
const blackPos = computed(() => calculatePosition(blackRef.value))
const blackStyle = computed(() => ({
  left: '240px',
  width: '120px',
  height: '310px',
  transform: isShowingPassword.value
    ? 'skewX(0deg)'  // 显示密码时，身体正常（背过去）
    : isLookingAtEachOther.value
      ? `skewX(${blackPos.value.bodySkew * 1.5 + 10}deg) translateX(20px)`
      : (props.isTyping || isHidingPassword.value)
        ? `skewX(${blackPos.value.bodySkew * 1.5}deg)`
        : `skewX(${blackPos.value.bodySkew}deg)`
}))
const blackEyesStyle = computed(() => ({
  left: isShowingPassword.value ? '10px' : isLookingAtEachOther.value ? '32px' : `${26 + blackPos.value.faceX}px`,
  top: isShowingPassword.value ? '28px' : isLookingAtEachOther.value ? '12px' : `${32 + blackPos.value.faceY}px`
}))
const blackForceLookX = computed(() => {
  if (isShowingPassword.value) return -4  // 显示密码时看向左边（不看）
  if (isLookingAtEachOther.value) return 0
  return undefined
})
const blackForceLookY = computed(() => {
  if (isShowingPassword.value) return -4
  if (isLookingAtEachOther.value) return -4
  return undefined
})

// Orange character styles
const orangePos = computed(() => calculatePosition(orangeRef.value))
const orangeStyle = computed(() => ({
  left: '0px',
  width: '240px',
  height: '200px',
  transform: isShowingPassword.value
    ? 'skewX(0deg)'  // 显示密码时，身体正常（背过去）
    : `skewX(${orangePos.value.bodySkew}deg)`
}))
const orangeEyesStyle = computed(() => ({
  left: isShowingPassword.value ? '50px' : `${82 + orangePos.value.faceX}px`,
  top: isShowingPassword.value ? '85px' : `${90 + orangePos.value.faceY}px`
}))
const orangeForceLookX = computed(() => isShowingPassword.value ? -5 : undefined)
const orangeForceLookY = computed(() => isShowingPassword.value ? -4 : undefined)

// Yellow character styles
const yellowPos = computed(() => calculatePosition(yellowRef.value))
const yellowStyle = computed(() => ({
  left: '310px',
  width: '140px',
  height: '230px',
  transform: isShowingPassword.value
    ? 'skewX(0deg)'  // 显示密码时，身体正常（背过去）
    : `skewX(${yellowPos.value.bodySkew}deg)`
}))
const yellowEyesStyle = computed(() => ({
  left: isShowingPassword.value ? '20px' : `${52 + yellowPos.value.faceX}px`,
  top: isShowingPassword.value ? '35px' : `${40 + yellowPos.value.faceY}px`
}))
const yellowMouthStyle = computed(() => ({
  left: isShowingPassword.value ? '10px' : `${40 + yellowPos.value.faceX}px`,
  top: isShowingPassword.value ? '88px' : `${88 + yellowPos.value.faceY}px`
}))
const yellowForceLookX = computed(() => isShowingPassword.value ? -5 : undefined)
const yellowForceLookY = computed(() => isShowingPassword.value ? -4 : undefined)
</script>

<style scoped>
.animated-characters {
  position: relative;
  width: 550px;
  height: 400px;
}

.character {
  position: absolute;
  bottom: 0;
  transition: all 0.7s ease-in-out;
  transform-origin: bottom center;
}

.character.purple {
  background-color: #6C3FF5;
  border-radius: 10px 10px 0 0;
  z-index: 1;
}

.character.black {
  background-color: #2D2D2D;
  border-radius: 8px 8px 0 0;
  z-index: 2;
}

.character.orange {
  background-color: #FF9B6B;
  border-radius: 120px 120px 0 0;
  z-index: 3;
}

.character.yellow {
  background-color: #E8D754;
  border-radius: 70px 70px 0 0;
  z-index: 4;
}

.eyes {
  position: absolute;
  display: flex;
  gap: 32px;
  transition: all 0.7s ease-in-out;
}

.eyes.pupils-only {
  gap: 32px;
}

.character.black .eyes {
  gap: 24px;
}

.character.yellow .eyes {
  gap: 24px;
}

.mouth {
  position: absolute;
  width: 80px;
  height: 4px;
  background-color: #2D2D2D;
  border-radius: 9999px;
  transition: all 0.2s ease-out;
}
</style>