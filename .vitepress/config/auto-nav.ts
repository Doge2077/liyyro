import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import type { DefaultTheme } from 'vitepress'

const docsDir = path.resolve(__dirname, '../../docs')

// 板块名称映射
const SECTION_MAP: Record<string, string> = {
  AI: 'AI',
  Life: '生活',
  History: '历史'
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

// 递归生成侧边栏项
function generateSidebarItems(dir: string, basePath: string): DefaultTheme.SidebarItem[] {
  const items: DefaultTheme.SidebarItem[] = []
  
  if (!fs.existsSync(dir)) return items
  
  // 获取子目录（支持自定义排序）
  const subDirs = fs.readdirSync(dir)
    .filter(d => {
      const fullPath = path.join(dir, d)
      return fs.statSync(fullPath).isDirectory()
    })
    .sort((a, b) => {
      // 检查是否有自定义排序配置
      const relPath = path.relative(docsDir, dir)
      const orderConfig = DIR_ORDER[relPath]
      if (orderConfig) {
        const orderA = orderConfig[a] ?? 999
        const orderB = orderConfig[b] ?? 999
        if (orderA !== orderB) return orderA - orderB
      }
      return a.localeCompare(b)
    })
  
  // 获取当前目录下的 .md 文件，按逻辑顺序排序
  const files = getMarkdownFiles(dir)
    .sort((a, b) => {
      // 先按 order 排序
      if (a.order !== b.order) {
        return a.order - b.order
      }
      // order 相同时按日期降序
      return b.date.getTime() - a.date.getTime()
    })
  
  // 添加子目录分组（默认收起）
  for (const subDir of subDirs) {
    const subPath = path.join(dir, subDir)
    const subItems = generateSidebarItems(subPath, `${basePath}/${subDir}`)
    
    if (subItems.length > 0) {
      items.push({
        text: subDir,
        collapsed: true,
        items: subItems
      })
    }
  }
  
  // 直接添加当前目录下的文件（不加"文章"层级）
  if (files.length > 0) {
    for (const f of files) {
      items.push({
        text: f.title,
        link: `${basePath}/${f.path}`
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
    .sort()
  
  return dirs.map(dir => ({
    text: SECTION_MAP[dir] || dir,
    link: `/${dir}/`
  }))
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
    .sort()

  for (const firstDir of firstLevelDirs) {
    const firstPath = path.join(docsDir, firstDir)
    const items = generateSidebarItems(firstPath, `/${firstDir}`)
    
    if (items.length > 0) {
      sidebar[`/${firstDir}/`] = items
    }
  }
  
  return sidebar
}
