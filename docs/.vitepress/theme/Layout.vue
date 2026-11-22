<script setup lang="ts">
import DefaultTheme from 'vitepress/theme-without-fonts'
import { useSidebar } from 'vitepress/theme-without-fonts'
import { onMounted, ref } from 'vue'

const { Layout } = DefaultTheme
const { hasSidebar } = useSidebar()

const STORAGE_KEY = 'kiyosi-sidebar-collapsed'
const isCollapsed = ref(false)

onMounted(() => {
  try {
    isCollapsed.value = localStorage.getItem(STORAGE_KEY) === 'true'
  } catch {
    // Ignore storage access errors in restricted environments.
  }
})

function toggleSidebarCollapse() {
  isCollapsed.value = !isCollapsed.value
  try {
    localStorage.setItem(STORAGE_KEY, String(isCollapsed.value))
  } catch {
    // Ignore storage access errors in restricted environments.
  }
}
</script>

<template>
  <div class="kiyosi-layout" :class="{ 'sidebar-collapsed': isCollapsed && hasSidebar }">
    <Layout>
      <template #nav-bar-content-before>
        <button
          v-if="hasSidebar"
          type="button"
          class="sidebar-collapse-btn"
          :aria-expanded="!isCollapsed"
          :aria-label="isCollapsed ? '展开侧边栏' : '收起侧边栏'"
          :title="isCollapsed ? '展开侧边栏' : '收起侧边栏'"
          @click="toggleSidebarCollapse"
        >
          <svg
            v-if="isCollapsed"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.75"
            stroke-linecap="round"
            stroke-linejoin="round"
            aria-hidden="true"
          >
            <rect x="3" y="3" width="18" height="18" rx="2" />
            <path d="M9 3v18" />
            <path d="m14 9 3 3-3 3" />
          </svg>
          <svg
            v-else
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.75"
            stroke-linecap="round"
            stroke-linejoin="round"
            aria-hidden="true"
          >
            <rect x="3" y="3" width="18" height="18" rx="2" />
            <path d="M9 3v18" />
            <path d="m16 15-3-3 3-3" />
          </svg>
        </button>
      </template>
    </Layout>
  </div>
</template>
