import { ref, computed } from 'vue'
import { data as postsData } from '../loaders/posts.data'

export interface Post {
  title: string
  date: string
  path: string
  description?: string
  categories?: string[]
  tags?: string[]
  section: string
}

const allPosts = ref<Post[]>(postsData || [])

export function usePosts(section?: string) {
  const posts = computed(() => {
    if (!section) return allPosts.value
    return allPosts.value.filter(p => p.section === section)
  })

  const pageSize = 10
  const currentPage = ref(1)
  
  const totalPages = computed(() => Math.ceil(posts.value.length / pageSize))
  
  const paginatedPosts = computed(() => {
    const start = (currentPage.value - 1) * pageSize
    return posts.value.slice(start, start + pageSize)
  })

  function goToPage(page: number) {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
    }
  }

  return {
    posts,
    paginatedPosts,
    currentPage,
    totalPages,
    goToPage
  }
}
