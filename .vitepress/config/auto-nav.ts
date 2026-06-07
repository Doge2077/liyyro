import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import type { DefaultTheme } from 'vitepress'

const docsDir = path.resolve(__dirname, '../../docs')

// 读取排序配置文件
const orderConfigPath = path.resolve(__dirname, '../../order.json')
let orderConfig: { sidebar?: Record<string, number>; directories?: Record<string, Record<string, number>> } = {}
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

// 目录Emoji映射
const EMOJI_MAP: Record<string, string> = {
  // History子目录
  'Algorithm': '🧠',
  'Cpp': '⚙️',
  'Cs-Fundamentals': '📚',
  'Database': '🗄️',
  'Java': '☕',
  'Linux': '🐧',
  'Python': '🐍',
  'Tips': '💡',
  // Life子目录
  'Articles': '📝',
  'Campus': '🏫',
  'Essays': '📖',
  'Novels': '📚',
  'Photos': '📷',
  'Poems': '🎭',
  // 算法子目录
  '算法讲解': '📖',
  '算法题解': '💻',
  '竞赛题解': '🏆',
  // 数据库子目录
  'mysql': '🐬',
  'neo4j': '🔗',
  'redis': '🔴',
  // Java子目录
  '架构': '🏗️',
  '其他': '📦',
  'jdk源码': '☕',
  'jvm': '☕',
  'spring': '🌱',
  // 计算机基础子目录
  '编译原理': '🔧',
  '计算机网络': '🌐',
  '计算机组成': '💻',
  '数据结构': '📊'
}

// 目录排序配置（数字越小越靠前）
const DIR_ORDER: Record<string, Record<string, number>> = {
  'History/algorithm': {
    '算法讲解': 1,
    '算法题解': 2,
    '竞赛题解': 3
  }
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
  // 匹配中文数字
  const chineseNums: Record<string, number> = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
    '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15
  }
  
  // 尝试匹配 "（一）" 或 "(一)" 格式
  const chineseMatch = title.match(/[（(]([一二三四五六七八九十]+)[）)]/)
  if (chineseMatch) {
    return chineseNums[chineseMatch[1]] || 999
  }
  
  // 尝试匹配数字格式如 "第1章" 或 "1." 或 "1-" 开头
  const numMatch = title.match(/^(?:第)?(\d+)[章节目篇.、-]/)
  if (numMatch) {
    return parseInt(numMatch[1])
  }
  
  // 尝试匹配标题中的第一个数字
  const firstNum = title.match(/\d+/)
  if (firstNum) {
    return parseInt(firstNum[0])
  }
  
  return 999 // 没有数字的排在最后
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

// 从名称中提取数字前缀用于排序
function extractOrderFromName(name: string): number {
  const match = name.match(/^(\d+)[.\s]/)
  return match ? parseInt(match[1]) : 999
}

// 递归生成侧边栏项
function generateSidebarItems(dir: string, basePath: string): DefaultTheme.SidebarItem[] {
  const items: DefaultTheme.SidebarItem[] = []
  
  if (!fs.existsSync(dir)) return items
  
  // 获取子目录
  const subDirs = fs.readdirSync(dir)
    .filter(d => {
      const fullPath = path.join(dir, d)
      return fs.statSync(fullPath).isDirectory()
    })
  
  // 获取当前目录下的 .md 文件
  const files = getMarkdownFiles(dir)
  
  // 合并子目录和文件，统一排序
  type Entry = { type: 'dir'; name: string } | { type: 'file'; name: string; title: string; path: string; order: number }
  const entries: Entry[] = [
    ...subDirs.map(d => ({ type: 'dir' as const, name: d })),
    ...files.map(f => ({ type: 'file' as const, name: f.name, title: f.title, path: f.path, order: f.order }))
  ]
  
  // 获取当前目录的相对路径（用于查找 orderConfig.directories）
  const relativePath = basePath.startsWith('/') ? basePath.slice(1) : basePath
  
  // 排序函数
  entries.sort((a, b) => {
    let orderA: number
    let orderB: number
    
    if (a.type === 'dir') {
      // 目录：优先使用 orderConfig.directories 配置
      const dirConfig = orderConfig.directories?.[relativePath]
      orderA = dirConfig?.[a.name] ?? extractOrderFromName(a.name)
    } else {
      // 文件：优先使用 frontmatter 的 order 字段
      orderA = (a.type === 'file' && a.order !== 999) ? a.order : 9999
    }
    
    if (b.type === 'dir') {
      const dirConfig = orderConfig.directories?.[relativePath]
      orderB = dirConfig?.[b.name] ?? extractOrderFromName(b.name)
    } else {
      orderB = (b.type === 'file' && b.order !== 999) ? b.order : 9999
    }
    
    if (orderA !== orderB) return orderA - orderB
    return a.name.localeCompare(b.name)
  })
  
  // 按排序顺序添加到 items
  for (const entry of entries) {
    if (entry.type === 'dir') {
      const subPath = path.join(dir, entry.name)
      const subItems = generateSidebarItems(subPath, `${basePath}/${entry.name}`)
      
      if (subItems.length > 0) {
        const emoji = EMOJI_MAP[entry.name] || ''
        const text = entry.name
        items.push({
          text: emoji ? `${emoji} ${text}` : text,
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
  
  const dirs = fs.readdirSync(docsDir)
    .filter(d => {
      const fullPath = path.join(docsDir, d)
      return fs.statSync(fullPath).isDirectory() && 
             d !== 'public' && 
             d !== '.vitepress' &&
             !d.startsWith('.')
    })
    .sort((a, b) => {
      const orderA = orderConfig.sidebar?.[a] ?? 9999
      const orderB = orderConfig.sidebar?.[b] ?? 9999
      if (orderA !== orderB) return orderA - orderB
      return a.localeCompare(b)
    })
  
  return dirs.map(dir => {
    const emoji = EMOJI_MAP[dir] || ''
    const text = SECTION_MAP[dir] || dir
    return {
      text: emoji ? `${emoji} ${text}` : text,
      link: `/${dir}/`
    }
  })
}

// 扫描目录 -> 生成 sidebar（支持多级）
export function generateSidebar(): DefaultTheme.Sidebar {
  if (!fs.existsSync(docsDir)) return {}
  
  const sidebar: DefaultTheme.Sidebar = {}
  const firstLevelDirs = fs.readdirSync(docsDir)
    .filter(d => {
      const fullPath = path.join(docsDir, d)
      return fs.statSync(fullPath).isDirectory() && 
             d !== 'public' && 
             d !== '.vitepress' &&
             !d.startsWith('.')
    })
    .sort((a, b) => {
      const orderA = orderConfig.sidebar?.[a] ?? 9999
      const orderB = orderConfig.sidebar?.[b] ?? 9999
      if (orderA !== orderB) return orderA - orderB
      return a.localeCompare(b)
    })

  for (const firstDir of firstLevelDirs) {
    const firstPath = path.join(docsDir, firstDir)
    const items = generateSidebarItems(firstPath, `/${firstDir}`)
    
    if (items.length > 0) {
      sidebar[`/${firstDir}/`] = items
    }
  }
  
  return sidebar
}
