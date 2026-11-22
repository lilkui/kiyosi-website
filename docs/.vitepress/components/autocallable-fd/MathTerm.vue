<script lang="ts">
import { ref } from 'vue'

const activeTermInstance = ref<string | null>(null)
</script>

<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, useId, watch } from 'vue'
import { MATH_TERMS } from './mathTerms'

const props = defineProps<{
  id: string
  title?: string
  en?: string
  detail?: string
}>()

const uid = useId()
const isMounted = ref(false)
const triggerRef = ref<HTMLButtonElement | null>(null)
const popoverRef = ref<HTMLDivElement | null>(null)

const coords = ref({
  top: 0,
  left: 0,
  arrowLeft: 24,
  placement: 'top' as 'top' | 'bottom',
  ready: false,
})

const entry = computed(() => MATH_TERMS[props.id])
const displayTitle = computed(() => props.title ?? entry.value?.title ?? props.id)
const displayEn = computed(() => props.en ?? entry.value?.en ?? '')
const displayHtml = computed(() => props.detail ?? entry.value?.html ?? '')

const isOpen = computed(() => isMounted.value && activeTermInstance.value === uid)

function updatePosition() {
  const trigger = triggerRef.value
  const popover = popoverRef.value
  if (!trigger || !popover) return

  const clientRects = trigger.getClientRects()
  const rect = clientRects.length > 0 ? clientRects[0] : trigger.getBoundingClientRect()
  const popRect = popover.getBoundingClientRect()

  const pad = 12
  const gap = 10
  const navHeight = 68
  const vw = window.innerWidth
  const vh = window.innerHeight

  const anchorX = rect.left + rect.width / 2
  let placement: 'top' | 'bottom' = 'top'
  let top = rect.top - popRect.height - gap

  if (top < navHeight && vh - rect.bottom > rect.top - navHeight) {
    placement = 'bottom'
    top = rect.bottom + gap
  } else if (top < pad) {
    top = pad
  }

  const maxLeft = Math.max(pad, vw - popRect.width - pad)
  const left = Math.min(Math.max(anchorX - popRect.width / 2, pad), maxLeft)
  const arrowLeft = Math.min(Math.max(anchorX - left, 18), Math.max(18, popRect.width - 18))

  coords.value = { top, left, arrowLeft, placement, ready: true }
}

function toggle() {
  if (activeTermInstance.value === uid) {
    activeTermInstance.value = null
  } else {
    coords.value.ready = false
    activeTermInstance.value = uid
  }
}

function close(restoreFocus = false) {
  if (activeTermInstance.value === uid) {
    activeTermInstance.value = null
    if (restoreFocus) {
      triggerRef.value?.focus()
    }
  }
}

function onPointerDownOutside(event: PointerEvent) {
  const target = event.target as Node | null
  if (!target) return
  if (triggerRef.value?.contains(target) || popoverRef.value?.contains(target)) {
    return
  }
  close(false)
}

function onKeyDown(event: KeyboardEvent) {
  if (event.key === 'Escape') {
    event.preventDefault()
    close(true)
  }
}

function addGlobalListeners() {
  window.addEventListener('scroll', updatePosition, { capture: true, passive: true })
  window.addEventListener('resize', updatePosition, { passive: true })
  document.addEventListener('pointerdown', onPointerDownOutside)
  document.addEventListener('keydown', onKeyDown)
}

function removeGlobalListeners() {
  if (typeof window === 'undefined') return
  window.removeEventListener('scroll', updatePosition, { capture: true })
  window.removeEventListener('resize', updatePosition)
  document.removeEventListener('pointerdown', onPointerDownOutside)
  document.removeEventListener('keydown', onKeyDown)
}

watch(isOpen, async (open) => {
  if (open) {
    await nextTick()
    updatePosition()
    addGlobalListeners()
  } else {
    coords.value.ready = false
    removeGlobalListeners()
  }
})

onMounted(() => {
  isMounted.value = true
})

onBeforeUnmount(() => {
  removeGlobalListeners()
  if (activeTermInstance.value === uid) {
    activeTermInstance.value = null
  }
})
</script>

<template>
  <button
    ref="triggerRef"
    type="button"
    class="fd-term"
    :class="{ 'is-open': isOpen }"
    :aria-expanded="isOpen ? 'true' : 'false'"
    :aria-controls="isOpen ? `fd-tip-${uid}` : undefined"
    title="点击查看名词释义"
    @click="toggle"
  >
    <slot>{{ displayTitle }}</slot>
  </button>
  <Teleport v-if="isOpen" to="body">
    <div
      :id="`fd-tip-${uid}`"
      ref="popoverRef"
      role="dialog"
      :aria-label="`${displayTitle} 名词释义`"
      class="fd-term-popover"
      :class="[`is-${coords.placement}`, { 'is-ready': coords.ready }]"
      :style="{
        top: `${coords.top}px`,
        left: `${coords.left}px`,
        '--fd-tip-arrow-x': `${coords.arrowLeft}px`,
      }"
    >
      <div class="fd-term-popover__head">
        <div class="fd-term-popover__titles">
          <span class="fd-term-popover__title">{{ displayTitle }}</span>
          <span v-if="displayEn" class="fd-term-popover__en">{{ displayEn }}</span>
        </div>
        <button
          type="button"
          class="fd-term-popover__close"
          aria-label="关闭释义"
          @click="close(true)"
        >
          ×
        </button>
      </div>
      <!-- eslint-disable-next-line vue/no-v-html -->
      <div class="fd-term-popover__body" v-html="displayHtml" />
    </div>
  </Teleport>
</template>
