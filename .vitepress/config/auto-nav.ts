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

// 扫描二级目录 -> 生成 sidebar
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
    
    // 获取二级目录
    const secondLevelDirs = fs.readdirSync(firstPath)
      .filter(d => {
        const fullPath = path.join(firstPath, d)
        return fs.statSync(fullPath).isDirectory()
      })
      .sort()
    
    // 获取一级目录下的直接 .md 文件
    const directFiles = getMarkdownFiles(firstPath)
      .sort((a, b) => b.date.getTime() - a.date.getTime())
    
    const items: DefaultTheme.SidebarItem[] = []
    
    // 添加二级目录分组
    for (const secondDir of secondLevelDirs) {
      const secondPath = path.join(firstPath, secondDir)
      const files = getMarkdownFiles(secondPath)
        .sort((a, b) => b.date.getTime() - a.date.getTime())
      
      if (files.length > 0) {
        items.push({
          text: secondDir,
          collapsed: false,
          items: files.map(f => ({
            text: f.title,
            link: `/${firstDir}/${secondDir}/${f.path}`
          }))
        })
      }
    }
    
    // 添加一级目录下的直接文件（不包括在子目录中的文件）
    if (directFiles.length > 0) {
      items.push({
        text: '文章',
        collapsed: false,
        items: directFiles.map(f => ({
          text: f.title,
          link: `/${firstDir}/${f.path}`
        }))
      })
    }
    
    if (items.length > 0) {
      sidebar[`/${firstDir}/`] = items
    }
  }
  
  return sidebar
}
