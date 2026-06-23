<template>
  <div class="typed-info">
    <span id="typedText" class="tagline"></span>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted } from 'vue';
import Typed from 'typed.js';

let typed;

onMounted(() => {
  typed = new Typed("#typedText", {
    strings: ["Welcome to Astria's Blog", 'Los perros románticos with King Shit on his throne of loneliness.'],
    startDelay: 300,
    backDelay: 2500,
    typeSpeed: 100,
    backSpeed: 100,
    loop: true,
    showCursor: true,
    cursorChar: '<span style="font-size: 24px; font-weight: 500;">▍</span>',
  });
})

onBeforeUnmount(() => {
  typed?.destroy();
})
</script>

<style scoped>
.typed-info {
  margin-top: 15px;
  min-height: 34px;
  overflow: visible;
}

.tagline {
  display: inline-block;
  padding-top: 8px;
  padding-bottom: 4px;
  max-width: 100%;
  line-height: 1.4;
  font-size: 18px;
  font-weight: 500;
  white-space: pre-wrap;
  overflow: visible;
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
