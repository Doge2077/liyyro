import { defineConfig } from 'vitepress'
import { zh, search as zhSearch } from './theme'
import footnote from 'markdown-it-footnote'
import markdownItMathjax3 from 'markdown-it-mathjax3'

export default defineConfig({
  outDir: 'dist',
  srcDir: 'docs',
  lastUpdated: true,
  ignoreDeadLinks: true,
  locales: {
    root: { label: '简体中文', ...zh }
  },
  themeConfig: {
    logo: '/logo/favicon.png',
    socialLinks: [
      { icon: 'github', link: 'https://github.com/Doge2077/liyyro' }
    ],
    search: {
      provider: 'local',
      options: {
        locales: { ...zhSearch }
      }
    }
  },
  markdown: {
    math: true,
    lineNumbers: true,
    image: {
      lazyLoading: true
    },
    headers: {
      level: [1, 2, 3]
    },
    config: (md) => {
      md.use(footnote)
      md.use(markdownItMathjax3)
    }
  },
  head: [
    ['link', { rel: 'preconnect', href: 'https://fonts.loli.net' }],
    ['link', { rel: 'preconnect', href: 'https://gstatic.loli.net', crossorigin: '' }],
    ['link', { href: 'https://fonts.loli.net/css2?family=Noto+Sans+SC:wght@400..900&display=swap', rel: 'stylesheet' }],
    ['link', { href: 'https://fonts.loli.net/css2?family=Fira+Code:wght@500&display=swap', rel: 'stylesheet' }],
    ['link', { rel: 'icon', href: '/logo/favicon.png' }]
  ]
})
