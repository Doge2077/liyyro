import { defineConfig } from 'vitepress'
import { zh, search as zhSearch } from './theme'
import footnote from 'markdown-it-footnote'
import mathjax3 from 'markdown-it-mathjax3'

const lowMemoryBuild = process.env.VITEPRESS_LOW_MEMORY_BUILD === 'true'

const escapeHtml = (value: string) =>
  value.replace(/[&<>"']/g, (char) => {
    switch (char) {
      case '&':
        return '&amp;'
      case '<':
        return '&lt;'
      case '>':
        return '&gt;'
      case '"':
        return '&quot;'
      default:
        return '&#39;'
    }
  })

const plainCodeHighlight = (code: string) => `<span v-pre>${escapeHtml(code)}</span>`

export default defineConfig({
  outDir: 'dist',
  srcDir: 'docs',
  mpa: process.env.VITEPRESS_MPA === 'true',
  lastUpdated: process.env.VITEPRESS_LAST_UPDATED === 'true',
  ignoreDeadLinks: true,
  locales: {
    root: { label: '简体中文', ...zh }
  },
  themeConfig: {
    logo: '/logo/favicon.png',
    socialLinks: [
      { icon: 'github', link: 'https://github.com/Doge2077/liyyro' }
    ],
    search: process.env.VITEPRESS_LOCAL_SEARCH === 'true'
      ? {
          provider: 'local',
          options: {
            locales: { ...zhSearch }
          }
        }
      : undefined
  },
  markdown: {
    cache: !lowMemoryBuild,
    highlight: lowMemoryBuild ? plainCodeHighlight : undefined,
    math: false,
    lineNumbers: !lowMemoryBuild,
    image: {
      lazyLoading: true
    },
    headers: {
      level: [1, 2, 3]
    },
    config: (md) => {
      md.use(footnote)
      md.use(mathjax3)

      const stripSideEffectTags = (render: any) => (...args: any[]) => {
        return render(...args).replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, '')
      }

      md.renderer.rules.math_inline = stripSideEffectTags(md.renderer.rules.math_inline)
      md.renderer.rules.math_block = stripSideEffectTags(md.renderer.rules.math_block)
    }
  },
  vite: {
    build: {
      minify: lowMemoryBuild ? false : 'esbuild',
      reportCompressedSize: false,
      cssCodeSplit: true,
      chunkSizeWarningLimit: 2000,
      rollupOptions: {
        cache: false
      }
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
