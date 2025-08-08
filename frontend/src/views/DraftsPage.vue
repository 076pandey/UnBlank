<template>
  <div class="min-h-screen bg-black text-white px-6 py-10">
    <h1 class="text-4xl font-bold mb-8 text-center">Your Drafts</h1>

    <div
      v-if="drafts.length"
      class="grid gap-6 md:grid-cols-2 lg:grid-cols-3 max-w-6xl mx-auto"
    >
      <div
        v-for="draft in drafts"
        :key="draft._id"
        class="bg-gray-900 rounded-xl p-6 hover:scale-[1.02] hover:shadow-lg transition"
      >
        <h2 class="text-2xl font-semibold mb-2">
          {{ draft.title || "Untitled Draft" }}
        </h2>
        <p class="text-gray-400 text-sm mb-4">Tone: {{ draft.tone || "—" }}</p>
        <p class="text-gray-300 mb-4 line-clamp-3">
          {{ draft.content || "No content yet..." }}
        </p>
        <button
          class="px-4 py-2 bg-white text-black rounded-full font-medium hover:bg-gray-300 transition"
          @click="editDraft(draft)"
        >
          Edit
        </button>
      </div>
    </div>

    <div v-else class="text-center text-gray-500 mt-20">
      No drafts saved yet.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const VITE_API_URL = import.meta.env.VITE_API_URL;
const router = useRouter();

const editDraft = (draft) => {
  localStorage.setItem("blogToEdit", JSON.stringify(draft));
  router.push("/write");
};

const drafts = ref([]);
const user_id = localStorage.getItem("user_id");

onMounted(async () => {
  try {
    const res = await axios.get(`${VITE_API_URL}/draft/${user_id}`);
    drafts.value = res.data.drafts;
  } catch (error) {
    console.error(error);
  }
});
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
