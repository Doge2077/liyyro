import { createContentLoader } from 'vitepress'

export interface Post {
  title: string
  date: string
  path: string
  description: string
  categories: string[]
  tags: string[]
  section: string
  order: number
}

export default createContentLoader(['AI/**/*.md', 'Life/**/*.md', 'History/**/*.md'], {
  excerpt: true,
  transform(rawData): Post[] {
    return rawData
      .filter(item => !item.url.endsWith('/'))
      .map(item => {
        const urlParts = item.url.split('/')
        const section = urlParts[1] || 'unknown'
        
        return {
          title: item.frontmatter.title || urlParts[urlParts.length - 1] || 'Untitled',
          date: item.frontmatter.date || '1970-01-01',
          path: item.url,
          description: item.frontmatter.description || '',
          categories: item.frontmatter.categories || [],
          tags: item.frontmatter.tags || [],
          section,
          order: item.frontmatter.order ?? 9999
        }
      })
      .sort((a, b) => {
        if (a.order !== b.order) return a.order - b.order
        // 如果 order 相同，按日期倒序
        return new Date(b.date).getTime() - new Date(a.date).getTime()
      })
  }
})
