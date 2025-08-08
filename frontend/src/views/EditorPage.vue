<template>
  <div
    class="min-h-screen bg-black text-white px-6 py-10 flex flex-col items-center"
  >
    <div class="w-full max-w-3xl">
      <!-- Topic Input -->
      <div class="mb-6">
        <label class="block mb-2 pt-10 text-gray-400"
          >What do you want to write about?</label
        >
        <input
          v-model="topic"
          type="text"
          placeholder="e.g. My breakup, leaving my job, feeling lost..."
          class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-3 text-white placeholder-gray-500"
        />
      </div>

      <!-- Title Input -->
      <input
        v-model="title"
        type="text"
        placeholder="Title your blog..."
        class="w-full bg-transparent border-b border-gray-600 text-3xl font-bold outline-none mb-6 placeholder-gray-500"
      />

      <!-- Tone Selector -->
      <div class="mb-6">
        <label class="block mb-2 text-gray-400">Tone</label>
        <select
          v-model="tone"
          class="bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 w-full text-white"
        >
          <option value="" disabled>Select tone</option>
          <option>Reflective</option>
          <option>Angry</option>
          <option>Grateful</option>
          <option>Heartbroken</option>
          <option>Custom</option>
        </select>
      </div>

      <!-- Visibility Selector -->
      <div class="mb-6">
        <label class="block mb-2 text-gray-400">Visibility</label>
        <div class="flex items-center gap-6">
          <label class="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              name="visibility"
              v-model="isPublic"
              :value="true"
              class="blue-accent"
            />
            <span>Public</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer">
            <input
              type="radio"
              name="visibility"
              v-model="isPublic"
              :value="false"
              class="blue-accent"
            />
            <span>Private</span>
          </label>
        </div>
      </div>

      <!-- AI Prompts -->
      <div v-if="prompts.length" class="mb-6">
        <p class="text-gray-400 mb-2">Here are some things to think about:</p>
        <ul class="space-y-2">
          <li
            v-for="(q, i) in prompts"
            :key="i"
            class="bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-gray-300"
          >
            💡 {{ q }}
          </li>
        </ul>
      </div>

      <!-- Blog Content Area -->
      <textarea
        v-model="content"
        rows="8"
        placeholder="Start writing here..."
        class="w-full bg-transparent border border-gray-700 rounded-lg px-4 py-3 text-lg outline-none placeholder-gray-500"
      ></textarea>

      <!-- Action Buttons -->
      <div class="flex justify-end mt-6 gap-4">
        <button
          class="px-5 py-2 bg-white text-black font-semibold rounded-full hover:bg-gray-300 transition"
          @click="generateWithAI"
        >
          Generate With AI
        </button>
        <button
          class="px-5 py-2 bg-white text-black font-semibold rounded-full hover:bg-gray-300 transition"
          @click="handleBlog"
        >
          Publish
        </button>
        <button
          class="px-5 py-2 border border-gray-600 rounded-full hover:bg-gray-800 transition"
          @click="saveAsDraft"
        >
          Save Draft
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import axios from "axios";

const title = ref("");
const tone = ref("");
const content = ref("");
const topic = ref("");
const prompts = ref([]);
const isPublic = ref(true);
const user_id = localStorage.getItem("user_id");
const isEditing = ref(false);
const blogId = ref(null);
const VITE_API_URL = import.meta.env.VITE_API_URL;


const loading = ref(false) 
const generateWithAI = async () => {
  if (!topic.value || !tone.value) {
    alert("Please provide a topic and tone.");
    return;
  }

  try {
    loading.value = true;
    const res = await axios.post(`${VITE_API_URL}/generate-blog`, {
      topic: topic.value,
      tone: tone.value,
    });

    content.value = res.data.blog;
  } catch (err) {
    console.error(err);
    alert("AI generation failed.");
  } finally {
    loading.value = false;
  }
};

const blogToEdit = JSON.parse(localStorage.getItem("blogToEdit"));
if (blogToEdit) {
  isEditing.value = true;
  blogId.value = blogToEdit._id;
  title.value = blogToEdit.title;
  tone.value = blogToEdit.tone;
  content.value = blogToEdit.content;
  topic.value = blogToEdit.topic;
  isPublic.value = blogToEdit.public;
  localStorage.removeItem("blogToEdit"); // cleanup
}

const resetFields = () => {
  title.value = "";
  tone.value = "";
  content.value = "";
  topic.value = "";
  prompts.value = [];
  isPublic.value = true;
  isEditing.value = false;
  blogId.value = null;
};

const createBlog = async () => {
  const res = await axios.post(`${VITE_API_URL}/blog`, {
    user_id,
    title: title.value,
    tone: tone.value,
    content: content.value,
    topic: topic.value,
    public: isPublic.value,
    published: true,
  });
  if (res.status === 200) {
    alert("Blog created successfully!");
    resetFields();
  }
};

const updateBlog = async () => {
  const res = await axios.put(`${VITE_API_URL}/blog/${blogId.value}`, {
    title: title.value,
    tone: tone.value,
    content: content.value,
    topic: topic.value,
    public: isPublic.value,
    published: true,
  });
  if (res.status === 200) {
    alert("Blog updated successfully!");
    resetFields();
  }
};

const handleBlog = async () => {
  if (!title.value.trim() || !content.value.trim() || !topic.value.trim()) {
    alert("Please fill in all the fields");
    return;
  }

  try {
    if (isEditing.value) {
      await updateBlog();
    } else {
      await createBlog();
    }
  } catch (error) {
    console.error(error);
    alert("Something went wrong.");
  }
};

const saveAsDraft = async () => {
  try {
    const payload = {
      user_id,
      title: title.value,
      tone: tone.value,
      content: content.value,
      topic: topic.value,
      public: isPublic.value,
      published: false,
    };

    if (isEditing.value) {
      await axios.put(`${VITE_API_URL}/blog/${blogId.value}`, payload);
      alert("Draft updated!");
    } else {
      await axios.post(`${VITE_API_URL}/blog`, payload);
      alert("Draft saved!");
    }
  } catch (error) {
    console.error("Failed to save draft:", error);
    alert("Something went wrong.");
  }
};

// Smart prompt generator
watch(topic, (val) => {
  if (!val.trim()) {
    prompts.value = [];
    return;
  }

  const lower = val.toLowerCase();
});
</script>

<style scoped></style>
