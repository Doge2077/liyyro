<template>
  <div class="blog-home">
    <div class="tab-bar">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        :class="['tab-btn', { active: activeTab === tab.key }]"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>
    
    <div class="post-list">
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="currentPosts.length === 0" class="empty">暂无文章</div>
      <article v-for="post in currentPosts" :key="post.path" class="post-item">
        <a :href="post.path" class="post-link">
          <div class="post-meta">
            <time :datetime="post.date">{{ formatDate(post.date) }}</time>
            <span v-if="post.categories?.length" class="categories">
              <span v-for="cat in post.categories" :key="cat" class="category-tag">{{ cat }}</span>
            </span>
          </div>
          <h3 class="post-title">{{ post.title }}</h3>
          <p v-if="post.description" class="post-desc">{{ post.description }}</p>
        </a>
      </article>
    </div>
    
    <div v-if="totalPages > 1" class="pagination">
      <button :disabled="currentPage <= 1" @click="goToPage(currentPage - 1)">←</button>
      <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
      <button :disabled="currentPage >= totalPages" @click="goToPage(currentPage + 1)">→</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { data as postsData } from '../loaders/posts.data'

interface Post {
  title: string
  date: string
  path: string
  description?: string
  categories?: string[]
  tags?: string[]
  section: string
  order: number
}

const tabs = [
  { key: 'AI', label: 'AI' },
  { key: 'Life', label: '生活' },
  { key: 'History', label: '历史' }
]

const activeTab = ref('AI')
const loading = ref(false)
const allPosts = ref<Post[]>(postsData || [])

const pageSize = 10
const currentPage = ref(1)

const filteredPosts = computed(() => {
  return allPosts.value.filter(p => p.section === activeTab.value)
})

const totalPages = computed(() => Math.ceil(filteredPosts.value.length / pageSize))

const currentPosts = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredPosts.value.slice(start, start + pageSize)
})

function goToPage(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

function formatDate(dateStr: string): string {
  const d = new Date(dateStr)
  return d.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

</script>

<style scoped>
.blog-home {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.tab-bar {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  border-bottom: 2px solid var(--vp-c-divider);
  padding-bottom: 12px;
}

.tab-btn {
  padding: 8px 20px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 16px;
  color: var(--vp-c-text-2);
  border-radius: 8px;
  transition: all 0.2s;
}

.tab-btn:hover {
  color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
}

.tab-btn.active {
  color: var(--vp-c-white);
  background: var(--vp-c-brand-1);
}

.post-list {
  min-height: 400px;
}

.post-item {
  margin-bottom: 16px;
  border-radius: 12px;
  transition: all 0.2s;
}

.post-item:hover {
  background: var(--vp-c-default-soft);
}

.post-link {
  display: block;
  padding: 16px 20px;
  text-decoration: none;
  color: inherit;
}

.post-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
  font-size: 14px;
  color: var(--vp-c-text-3);
}

.category-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
  font-size: 12px;
}

.post-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.post-desc {
  margin: 8px 0 0;
  font-size: 14px;
  color: var(--vp-c-text-2);
  line-height: 1.6;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 32px;
  padding-top: 20px;
  border-top: 1px solid var(--vp-c-divider);
}

.pagination button {
  padding: 8px 16px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg);
  cursor: pointer;
  border-radius: 6px;
  color: var(--vp-c-text-1);
  transition: all 0.2s;
}

.pagination button:hover:not(:disabled) {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: var(--vp-c-text-2);
}

.loading, .empty {
  text-align: center;
  padding: 40px;
  color: var(--vp-c-text-3);
}
</style>
