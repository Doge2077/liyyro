import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import type { DefaultTheme } from 'vitepress'

const docsDir = path.resolve(__dirname, '../../docs')

// 读取排序配置文件（嵌套格式）
const orderConfigPath = path.resolve(__dirname, '../../order.json')
let orderConfig: Record<string, any> = {}
try {
  if (fs.existsSync(orderConfigPath)) {
    orderConfig = JSON.parse(fs.readFileSync(orderConfigPath, 'utf-8'))
  }
} catch (e) {
  console.warn('Failed to load order.json:', e)
}

// 板块名称映射
const SECTION_MAP: Record<string, string> = {
  AI: 'AI',
  Life: 'Life',
  History: 'History'
}

// 侧边栏一级目录 Emoji（仅顶层使用）
const SIDEBAR_EMOJI_MAP: Record<string, string> = {
  'AI': '🤖',
  'Life': '🌟',
  'History': '📚',
  // History 子目录
  'algorithm': '🧠',
  'java': '☕',
  'cpp': '⚙️',
  'cs-fundamentals': '📚',
  'database': '🗄️',
  'python': '🐍',
  'linux': '🐧',
  'tips': '💡',
  'other': '📦',
  // 算法子目录
  '算法讲解': '📖',
  '算法题解': '💻',
  '竞赛题解': '🏆',
  // 数据库子目录
  'mysql': '🐬',
  'redis': '🔴',
  'neo4j': '🔗',
  // Java子目录
  'jdk源码': '☕',
  'jvm': '☕',
  'spring': '🌱',
  '架构': '🏗️',
  '其他': '📦',
  // 计算机基础子目录
  '数据结构': '📊',
  '计算机组成': '💻',
  '编译原理': '🔧',
  '计算机网络': '🌐'
}

interface MarkdownFile {
  name: string
  title: string
  date: Date
  path: string
  order: number
}

// 从标题中提取数字（用于排序）
function extractNumber(title: string): number {
  const chineseNums: Record<string, number> = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
    '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15
  }
  const chineseMatch = title.match(/[（(]([一二三四五六七八九十]+)[）)]/)
  if (chineseMatch) return chineseNums[chineseMatch[1]] || 999
  const numMatch = title.match(/^(?:第)?(\d+)[章节目篇.、-]/)
  if (numMatch) return parseInt(numMatch[1])
  const firstNum = title.match(/\d+/)
  if (firstNum) return parseInt(firstNum[0])
  return 999
}

// 从名称中提取数字前缀
function extractOrderFromName(name: string): number {
  const match = name.match(/^(\d+)[.\s]/)
  return match ? parseInt(match[1]) : 999
}

// 从嵌套配置中获取某个目录的排序数组
function getOrderArray(configPath: string): string[] {
  const parts = configPath.split('/')
  let current: any = orderConfig
  for (const part of parts) {
    if (current && typeof current === 'object' && part in current) {
      current = current[part]
    } else {
      return []
    }
  }
  if (current && typeof current === 'object' && '_order' in current) {
    return current['_order']
  }
  return []
}

// 获取指定目录下的 .md 文件（不递归，排除 index.md）
function getMarkdownFiles(dir: string): MarkdownFile[] {
  const files: MarkdownFile[] = []
  if (!fs.existsSync(dir)) return files

  for (const f of fs.readdirSync(dir)) {
    const fullPath = path.join(dir, f)
    if (fs.statSync(fullPath).isDirectory()) continue
    if (!f.endsWith('.md') || f === 'index.md') continue

    try {
      const content = fs.readFileSync(fullPath, 'utf-8')
      const { data } = matter(content)
      const name = f.replace('.md', '')
      const title = data.title || name
      files.push({
        name,
        title,
        date: data.date ? new Date(data.date) : new Date(0),
        path: name,
        order: data.order || extractNumber(title)
      })
    } catch {
      const name = f.replace('.md', '')
      files.push({
        name,
        title: name,
        date: new Date(0),
        path: name,
        order: extractNumber(name)
      })
    }
  }
  return files
}

// 根据 _order 数组排序
function sortByOrder<T extends { name: string }>(items: T[], orderArr: string[]): T[] {
  if (!orderArr || orderArr.length === 0) return items
  const orderMap = new Map(orderArr.map((name, idx) => [name, idx]))
  return [...items].sort((a, b) => {
    const idxA = orderMap.has(a.name) ? orderMap.get(a.name)! : 9999
    const idxB = orderMap.has(b.name) ? orderMap.get(b.name)! : 9999
    if (idxA !== idxB) return idxA - idxB
    return a.name.localeCompare(b.name)
  })
}

// 递归生成侧边栏项
function generateSidebarItems(dir: string, basePath: string): DefaultTheme.SidebarItem[] {
  const items: DefaultTheme.SidebarItem[] = []
  if (!fs.existsSync(dir)) return items

  // 获取子目录
  const subDirs = fs.readdirSync(dir)
    .filter(d => fs.statSync(path.join(dir, d)).isDirectory())

  // 获取当前目录下的 .md 文件
  const files = getMarkdownFiles(dir)

  // 计算 order.json 中的配置路径
  const relBasePath = basePath.startsWith('/') ? basePath.slice(1) : basePath

  // 用 _order 排序子目录
  const dirOrderArr = getOrderArray(relBasePath)
  const sortedDirs = sortByOrder(
    subDirs.map(d => ({ name: d })),
    dirOrderArr
  ).map(d => d.name)

  // 用 _order 或 frontmatter order 排序文件
  const fileOrderArr = getOrderArray(relBasePath)
  const sortedFiles = sortByOrder(
    files.map(f => ({ ...f })),
    fileOrderArr
  ).sort((a, b) => {
    // 如果在 _order 中有位置，按 _order 排
    const idxA = fileOrderArr.indexOf(a.name)
    const idxB = fileOrderArr.indexOf(b.name)
    if (idxA !== -1 && idxB !== -1) return idxA - idxB
    if (idxA !== -1) return -1
    if (idxB !== -1) return 1
    // 否则按 order 字段排
    if (a.order !== b.order) return a.order - b.order
    return b.date.getTime() - a.date.getTime()
  })

  // 合并子目录和文件，按 _order 统一排序
  type Entry = { type: 'dir'; name: string } | { type: 'file'; name: string; title: string; path: string; order: number }
  const entries: Entry[] = [
    ...sortedDirs.map(d => ({ type: 'dir' as const, name: d })),
    ...sortedFiles.map(f => ({ type: 'file' as const, name: f.name, title: f.title, path: f.path, order: f.order }))
  ]

  // 如果有 _order，按 _order 统一排序
  if (fileOrderArr.length > 0) {
    const orderMap = new Map(fileOrderArr.map((name, idx) => [name, idx]))
    entries.sort((a, b) => {
      const idxA = orderMap.has(a.name) ? orderMap.get(a.name)! : 9999
      const idxB = orderMap.has(b.name) ? orderMap.get(b.name)! : 9999
      if (idxA !== idxB) return idxA - idxB
      return a.name.localeCompare(b.name)
    })
  }

  // 按排序顺序添加到 items
  for (const entry of entries) {
    if (entry.type === 'dir') {
      const subPath = path.join(dir, entry.name)
      const subItems = generateSidebarItems(subPath, `${basePath}/${entry.name}`)
      if (subItems.length > 0) {
        // 一级目录添加 emoji
        const emoji = SIDEBAR_EMOJI_MAP[entry.name] || ''
        const text = emoji ? `${emoji} ${entry.name}` : entry.name
        items.push({
          text,
          collapsed: true,
          items: subItems
        })
      }
    } else {
      items.push({
        text: entry.title,
        link: `${basePath}/${entry.path}`
      })
    }
  }

  return items
}

// 扫描一级目录 -> 生成 nav
export function generateNav(): DefaultTheme.NavItem[] {
  if (!fs.existsSync(docsDir)) return []

  const topOrder: string[] = orderConfig.topLevel || []
  const dirs = fs.readdirSync(docsDir)
    .filter(d => {
      const fullPath = path.join(docsDir, d)
      return fs.statSync(fullPath).isDirectory() &&
             d !== 'public' &&
             d !== '.vitepress' &&
             !d.startsWith('.')
    })

  const sortedDirs = sortByOrder(dirs.map(d => ({ name: d })), topOrder).map(d => d.name)

  return sortedDirs.map(dir => {
    const text = SECTION_MAP[dir] || dir
    return {
      text,
      link: `/${dir}/`
    }
  })
}

// 扫描目录 -> 生成 sidebar（支持多级）
export function generateSidebar(): DefaultTheme.Sidebar {
  if (!fs.existsSync(docsDir)) return {}

  const sidebar: DefaultTheme.Sidebar = {}
  const topOrder: string[] = orderConfig.topLevel || []
  const firstLevelDirs = fs.readdirSync(docsDir)
    .filter(d => {
      const fullPath = path.join(docsDir, d)
      return fs.statSync(fullPath).isDirectory() &&
             d !== 'public' &&
             d !== '.vitepress' &&
             !d.startsWith('.')
    })

  const sortedDirs = sortByOrder(firstLevelDirs.map(d => ({ name: d })), topOrder).map(d => d.name)

  for (const firstDir of sortedDirs) {
    const firstPath = path.join(docsDir, firstDir)
    const items = generateSidebarItems(firstPath, `/${firstDir}`)
    if (items.length > 0) {
      const emoji = SIDEBAR_EMOJI_MAP[firstDir] || ''
      const text = emoji ? `${emoji} ${firstDir}` : firstDir
      sidebar[`/${firstDir}/`] = items
    }
  }

  return sidebar
}
