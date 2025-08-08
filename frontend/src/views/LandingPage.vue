<template>
  <div class="min-h-screen bg-gradient-to-br from-[#1f1f1f] via-[#111111] to-black text-white flex flex-col items-center justify-center px-6">
    <h1 class="text-5xl md:text-7xl font-bold mb-4 text-center">
      UnBlank
    </h1>
    <p class="text-lg md:text-2xl text-gray-300 text-center max-w-2xl mb-8">
      Your space to write. Reflect. Connect. Stay anonymous or go public. Write like it matters.
    </p>

    <!-- Buttons -->
    <div class="flex gap-4">
      <button class="bg-white text-black px-6 py-2 rounded-full text-lg font-semibold hover:bg-gray-200 transition"
      @click="$router.push('/login')"
      >
        Get Started
      </button>
      <button
        @click="showMore = !showMore"
        class="border border-gray-500 text-white px-6 py-2 rounded-full text-lg hover:bg-white hover:text-black transition"
      >
        Learn More
      </button>
    </div>

    <!-- Learn More Section with Fade -->
    <transition name="fade">
      <div v-show="showMore" class="relative mt-8 max-w-2xl w-full text-center text-gray-300 text-base md:text-lg bg-[#1a1a1a] p-6 rounded-xl border border-gray-700">
        <!-- Close Button -->
        <button
          @click="showMore = false"
          class="absolute top-3 right-4 text-gray-400 hover:text-white text-xl font-bold"
        >
          &times;
        </button>

        <p>
          <strong class="text-white">UnBlank</strong> is an AI-guided writing and publishing platform that helps people turn raw thoughts into meaningful blogs — not through templates or formulas, but through questions.
        </p>
        <p class="mt-4">
          Whether you’re reflecting on your day, reviewing a book, thinking about death, or ranting about tech — UnBlank meets you with the right tone, the right prompts, and the right space.
        </p>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const showMore = ref(false)
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.fade-enter-to, .fade-leave-from {
  opacity: 1;
}
</style>
