<template>
  <footer class="blog-footer">
    <div class="footer-content">
      <p>&copy; {{ year }} lys2021. All rights reserved.</p>
      <p class="footer-links">
        <a href="https://github.com/Doge2077" target="_blank">GitHub</a>
        <span class="divider">|</span>
        <a href="https://lys2021.com" target="_blank">WordPress</a>
      </p>
    </div>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
</script>

<style scoped>
.blog-footer {
  margin-top: 40px;
  padding: 24px 0;
  border-top: 1px solid var(--vp-c-divider);
  text-align: center;
}

.footer-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-content p {
  margin: 4px 0;
  font-size: 14px;
  color: var(--vp-c-text-3);
}

.footer-links a {
  color: var(--vp-c-text-2);
  text-decoration: none;
  transition: color 0.2s;
}

.footer-links a:hover {
  color: var(--vp-c-brand-1);
}

.divider {
  margin: 0 8px;
  color: var(--vp-c-divider);
}
</style>
