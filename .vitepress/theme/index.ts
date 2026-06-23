import { h } from 'vue'
import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme-without-fonts'

import './style.css'

import Footer from './components/Footer.vue'
import TypedInfo from './components/TypedInfo.vue'

declare global {
  interface Window {
    MathJax?: {
      typesetPromise?: () => Promise<void>
    }
  }
}

const typesetMath = () => {
  if (typeof window === 'undefined') {
    return
  }

  window.requestAnimationFrame(() => {
    window.MathJax?.typesetPromise?.()
  })
}

export default {
  extends: DefaultTheme,
  enhanceApp({ router }) {
    router.onAfterRouteChanged = typesetMath
  },
  Layout: () => {
    return h(DefaultTheme.Layout, null, {
      'layout-bottom': () => h(Footer),
      'home-hero-info-after': () => h(TypedInfo)
    })
  }
} satisfies Theme
