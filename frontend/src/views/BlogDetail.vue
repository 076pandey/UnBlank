<template>
  <div class="min-h-screen bg-black text-white px-6 py-10 max-w-3xl mx-auto">
    <button @click="$router.back()" class="text-sm text-gray-400 mb-4 hover:underline">
      ← Back
    </button>

    <div v-if="blog">
      <h1 class="text-4xl font-bold mb-2">{{ blog.title }}</h1>
      <p class="text-gray-400 text-sm mb-4">Tone: {{ blog.tone }}</p>
      <p class="text-gray-300 whitespace-pre-line">{{ blog.content }}</p>
    </div>

    <div v-else class="text-center text-gray-500">
      Loading blog...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';


const VITE_API_URL = import.meta.env.VITE_API_URL;
const route = useRoute();
const blog = ref(null);

onMounted(async () => {
  const id = route.params.id;

  try {
    const res = await axios.get(`${VITE_API_URL}/single-blog/${id}`);
    blog.value = res.data.blog;
  } catch (err) {
    console.error("Failed to fetch blog:", err);
  }
});
</script>
