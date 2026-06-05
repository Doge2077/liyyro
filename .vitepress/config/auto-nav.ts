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

interface MarkdownFile {
  name: string
  title: string
  date: Date
  path: string
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
      files.push({
        name,
        title: data.title || name,
        date: data.date ? new Date(data.date) : new Date(0),
        path: name
      })
    } catch {
      const name = f.replace('.md', '')
      files.push({
        name,
        title: name,
        date: new Date(0),
        path: name
      })
    }
  }
  return files
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
    .sort()
  
  // 获取当前目录下的 .md 文件
  const files = getMarkdownFiles(dir)
    .sort((a, b) => b.date.getTime() - a.date.getTime())
  
  // 添加子目录分组
  for (const subDir of subDirs) {
    const subPath = path.join(dir, subDir)
    const subItems = generateSidebarItems(subPath, `${basePath}/${subDir}`)
    
    if (subItems.length > 0) {
      items.push({
        text: subDir,
        collapsed: false,
        items: subItems
      })
    }
  }
  
  // 添加当前目录下的文件
  if (files.length > 0) {
    items.push({
      text: '文章',
      collapsed: false,
      items: files.map(f => ({
        text: f.title,
        link: `${basePath}/${f.path}`
      }))
    })
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
