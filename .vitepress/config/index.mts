import { defineConfig } from 'vitepress'
import { zh, search as zhSearch } from './theme'
import footnote from 'markdown-it-footnote'

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

const isEscaped = (src: string, pos: number) => {
  let count = 0
  for (let index = pos - 1; index >= 0 && src[index] === '\\'; index--) {
    count++
  }
  return count % 2 === 1
}

const useLightweightMath = (md: any) => {
  md.inline.ruler.after('escape', 'math_inline', (state: any, silent: boolean) => {
    if (state.src[state.pos] !== '$' || state.src[state.pos + 1] === '$') {
      return false
    }

    const start = state.pos + 1
    let match = start

    while ((match = state.src.indexOf('$', match)) !== -1) {
      if (!isEscaped(state.src, match)) {
        const followingChar = state.src.charCodeAt(match + 1)
        if (!(followingChar >= 48 && followingChar <= 57)) {
          break
        }
      }
      match++
    }

    if (match === -1 || match === start || !state.src.slice(start, match).trim()) {
      return false
    }

    if (!silent) {
      const token = state.push('math_inline', 'math', 0)
      token.markup = '$'
      token.content = state.src.slice(start, match)
    }

    state.pos = match + 1
    return true
  })

  md.block.ruler.after('blockquote', 'math_block', (state: any, startLine: number, endLine: number, silent: boolean) => {
    let pos = state.bMarks[startLine] + state.tShift[startLine]
    let max = state.eMarks[startLine]

    if (pos + 2 > max || state.src.slice(pos, pos + 2) !== '$$') {
      return false
    }

    if (silent) {
      return true
    }

    pos += 2
    let firstLine = state.src.slice(pos, max)
    let lastLine = ''
    let nextLine = startLine
    let found = false

    if (firstLine.trim().endsWith('$$')) {
      firstLine = firstLine.trim().slice(0, -2)
      found = true
    }

    while (!found) {
      nextLine++
      if (nextLine >= endLine) {
        break
      }

      pos = state.bMarks[nextLine] + state.tShift[nextLine]
      max = state.eMarks[nextLine]

      if (pos < max && state.tShift[nextLine] < state.blkIndent) {
        break
      }

      const currentLine = state.src.slice(pos, max)
      if (currentLine.trim().endsWith('$$')) {
        lastLine = currentLine.slice(0, currentLine.lastIndexOf('$$'))
        found = true
      }
    }

    state.line = nextLine + 1

    const token = state.push('math_block', 'math', 0)
    token.block = true
    token.content = [
      firstLine && firstLine.trim() ? firstLine : '',
      state.getLines(startLine + 1, nextLine, state.tShift[startLine], true),
      lastLine && lastLine.trim() ? lastLine : ''
    ].filter(Boolean).join('\n')
    token.map = [startLine, state.line]
    token.markup = '$$'

    return true
  }, {
    alt: ['paragraph', 'reference', 'blockquote', 'list']
  })

  md.renderer.rules.math_inline = (tokens: any[], idx: number) =>
    `<span v-pre class="math math-inline">\\(${escapeHtml(tokens[idx].content)}\\)</span>`

  md.renderer.rules.math_block = (tokens: any[], idx: number) =>
    `<div v-pre class="math math-display">\\[${escapeHtml(tokens[idx].content)}\\]</div>`
}

export default defineConfig({
  outDir: 'dist',
  srcDir: 'docs',
  mpa: process.env.VITEPRESS_MPA === 'true',
  metaChunk: true,
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
    ...(lowMemoryBuild ? {
      cache: false,
      highlight: plainCodeHighlight,
      lineNumbers: false
    } : {
      cache: true,
      lineNumbers: true
    }),
    math: false,
    image: {
      lazyLoading: true
    },
    headers: {
      level: [1, 2, 3]
    },
    config: (md) => {
      md.use(footnote)
      useLightweightMath(md)
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
    ['script', {}, `window.MathJax = {
  tex: {
    inlineMath: [['\\\\(', '\\\\)']],
    displayMath: [['\\\\[', '\\\\]']]
  },
  svg: { fontCache: 'global' }
};`],
    ['script', { id: 'MathJax-script', async: '', src: 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js' }],
    ['link', { rel: 'icon', href: '/logo/favicon.png' }]
  ]
})
