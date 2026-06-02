import { h } from 'vue'
import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme-without-fonts'

import './style.css'

import Footer from './components/Footer.vue'
import BlogHome from './components/BlogHome.vue'

export default {
  extends: DefaultTheme,
  Layout: () => {
    return h(DefaultTheme.Layout, null, {
      'layout-bottom': () => h(Footer),
      'home-features-after': () => h(BlogHome)
    })
  }
} satisfies Theme
