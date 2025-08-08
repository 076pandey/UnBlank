<template>
  <div class="min-h-screen bg-black text-white px-6 py-10">
    <h1 class="text-4xl font-bold mb-8 text-center">
      {{ isPrivate ? "Private Blogs" : "Explore Blogs" }}
    </h1>

    <!-- Blog Grid -->
    <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3 max-w-6xl mx-auto">
      <div
        v-for="blog in blogs"
        :key="blog._id"
        class="bg-gray-900 rounded-xl p-6 hover:scale-[1.02] hover:shadow-lg transition"
      >
        <h2 class="text-2xl font-semibold mb-2">{{ blog.title }}</h2>
        <p class="text-gray-400 text-sm mb-4">Tone: {{ blog.tone }}</p>

        <!-- Content with Read More toggle -->
        <p
          :class="[
            'text-gray-300 mb-4',
            !expandedBlogs[blog._id] ? 'line-clamp-3' : ''
          ]"
        >
          {{ blog.content }}
        </p>

        <!-- Read More / Read Less Button -->
        <button
          v-if="blog.content.length > 200"
          @click="toggleReadMore(blog._id)"
          class="px-4 py-2 bg-white text-black rounded-full font-medium hover:bg-gray-300 transition"
        >
          {{ expandedBlogs[blog._id] ? "Read Less" : "Read More" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
const VITE_API_URL = import.meta.env.VITE_API_URL;

const blogs = ref([]);
const route = useRoute();
const isPrivate = ref(false);

// Stores which blogs are expanded
const expandedBlogs = ref({});

// Toggle Read More state
const toggleReadMore = (id) => {
  expandedBlogs.value[id] = !expandedBlogs.value[id];
};

onMounted(async () => {
  const user_id = localStorage.getItem("user_id");

  if (!user_id) {
    alert("Please login to view blogs");
    return;
  }

  if (route.path === '/private') {
    isPrivate.value = true;
    await fetchPrivateBlogs(user_id);
  } else {
    isPrivate.value = false;
    await fetchPublicBlogs();
  }
});

const fetchPublicBlogs = async () => {
  try {
    const res = await axios.get(`${VITE_API_URL}/blog-feed`);
    blogs.value = res.data;
    console.log("Fetched blogs:", blogs.value);
  } catch (err) {
    console.error(err);
    alert("There is some problem with getting blogs.");
  }
};

const fetchPrivateBlogs = async (user_id) => {
  try {
    const res = await axios.get(`${VITE_API_URL}/private-blogs/${user_id}`);
    blogs.value = res.data;
    console.log("Fetched blogs:", blogs.value);
  } catch (err) {
    console.error(err);
    alert("Failed to load private blogs.");
  }
};
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
