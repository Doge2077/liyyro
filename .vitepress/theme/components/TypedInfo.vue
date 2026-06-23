<template>
  <div class="typed-info">
    <span id="typedText" class="tagline"></span>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import Typed from 'typed.js';

onMounted(() => {
  new Typed("#typedText", {
    strings: ["Welcome to Astraia's Blog", 'Los perros románticos with King Shit on his throne of loneliness.'],
    startDelay: 300,
    backDelay: 2500,
    typeSpeed: 100,
    backSpeed: 100,
    loop: true,
    showCursor: true,
    cursorChar: '<span style="font-size: 24px; font-weight: 500;">▍</span>',
  });
})
</script>

<style scoped>
.typed-info {
  margin-top: 15px;
}

.tagline {
  padding-top: 8px;
  max-width: 392px;
  line-height: 28px;
  font-size: 18px;
  font-weight: 500;
  white-space: pre-wrap;
  color: var(--vp-c-text-2);
}

@media (min-width: 640px) {
  .tagline {
    font-size: 20px;
  }
}

@media (min-width: 960px) {
  .tagline {
    font-size: 22px;
  }
}
</style>
