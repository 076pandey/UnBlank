<template>
  <div class="min-h-screen bg-black text-white px-6 py-10 relative">
    <button
      @click="deleteAccount"
      class="absolute top-6 right-36 bg-red-500 text-white px-4 py-2 rounded-full text-sm hover:bg-red-600 transition"
    >
      Delete Account
    </button>

    <button
      @click="logout"
      class="absolute top-6 right-6 bg-red-600 text-white px-4 py-2 rounded-full text-sm hover:bg-red-700 transition"
    >
      Logout
    </button>

    <div class="max-w-4xl mx-auto">
      <!-- ✅ Profile Avatar -->
      <div class="flex flex-col items-center justify-center mb-6">
        <img
          :src="`https://api.dicebear.com/7.x/thumbs/svg?seed=${avatarSeed}`"
          alt="Profile Avatar"
          class="w-24 h-24 rounded-full border-2 border-gray-600 shadow-md"
        />
        <p class="mt-2 text-gray-400 text-sm">{{ username }}</p>
      </div>

      <!-- Blogs Section -->
      <h1 class="text-4xl font-bold mb-8 text-center">Your Blogs</h1>

      <!-- No Blogs or Error -->
      <div v-if="errorMsg" class="text-center text-gray-500 text-lg mt-6">
        {{ errorMsg }}
      </div>

      <div class="grid gap-6">
        <div
          v-for="blog in blogs"
          :key="blog._id"
          class="bg-gray-900 p-6 rounded-xl flex flex-col md:flex-row justify-between items-start md:items-center"
        >
          <div class="mb-4 md:mb-0">
            <h2 class="text-2xl font-semibold">{{ blog.title }}</h2>
            <p class="text-gray-400 text-sm mt-1">Tone: {{ blog.tone }}</p>
            <p class="text-sm mt-1 text-gray-500">
              Visibility:
              <span :class="blog.public ? 'text-green-400' : 'text-red-400'">
                {{ blog.public ? "Public" : "Private" }}
              </span>
            </p>
          </div>

          <div class="flex gap-4">
            <button
              class="px-4 py-1 border border-gray-600 rounded-full text-sm hover:bg-gray-800 transition"
              @click="editBlog(blog)"
            >
              Edit
            </button>

            <button
              class="px-4 py-1 bg-white text-black rounded-full text-sm hover:bg-gray-300 transition"
              @click="$router.push(`/blog/${blog._id}`)"
            >
              View
            </button>

            <button
              class="px-4 py-1 bg-red-600 text-white rounded-full text-sm hover:bg-red-700 transition"
              @click="deleteBlog(blog._id)"
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();

const blogs = ref([]);
const avatarSeed = ref("");
const username = ref("");
const errorMsg = ref("");
const VITE_API_URL = import.meta.env.VITE_API_URL;


const deleteAccount = async () => {
  const userId = localStorage.getItem("user_id");

  if (!userId) {
    alert("User ID not found. Please login again.");
    return;
  }

  const confirmDelete = confirm(
    "Are you sure you want to delete your account and all blogs? This action is permanent."
  );
  if (!confirmDelete) return;

  try {
    const res = await axios.delete(
      `${VITE_API_URL}/delete-user/${userId}`
    );
    alert("Account and all blogs deleted.");

    // Clear localStorage and redirect
    localStorage.clear();
    router.push("/");
  } catch (err) {
    console.error("Account deletion failed:", err);
    alert("Something went wrong. Could not delete your account.");
  }
};

// ✅ Delete Blog
const deleteBlog = async (id) => {
  const confirmDelete = confirm("Are you sure you want to delete this blog?");
  if (!confirmDelete) return;

  try {
    await axios.delete(`${VITE_API_URL}/blog/${id}`);
    blogs.value = blogs.value.filter((blog) => blog._id !== id);
    alert("Blog deleted successfully.");
  } catch (error) {
    console.error("Failed to delete blog:", error);
    alert("Failed to delete the blog.");
  }
};

const editBlog = (blog) => {
  localStorage.setItem("blogToEdit", JSON.stringify(blog));
  router.push("/write");
};

const logout = () => {
  localStorage.removeItem("user_id");
  localStorage.removeItem("username");
  localStorage.removeItem("unblank_avatar_seed");
  localStorage.clear();
  router.push("/login");
};

onMounted(async () => {
  const storedUsername = localStorage.getItem("username");
  if (storedUsername) {
    username.value = storedUsername;
  }

  const savedSeed = localStorage.getItem("unblank_avatar_seed");
  if (savedSeed) {
    avatarSeed.value = savedSeed;
  } else {
    const newSeed = "user_" + Math.random().toString(36).substring(2, 10);
    localStorage.setItem("unblank_avatar_seed", newSeed);
    avatarSeed.value = newSeed;
  }

  const userId = localStorage.getItem("user_id");
  if (!userId || userId.length !== 24) {
    errorMsg.value = "Please login to view your blogs.";
    router.push("/login");
    return;
  }

  try {
    const res = await axios.get(`${VITE_API_URL}/blog/${userId}`);
    blogs.value = res.data.blogs;

    if (res.data.username) {
      localStorage.setItem("username", res.data.username);
      username.value = res.data.username;
    }

    if (res.data.blogs.length === 0) {
      errorMsg.value = "You haven’t written any blogs yet.";
    }
  } catch (error) {
    console.error("Error fetching blogs:", error);
    errorMsg.value = "Failed to fetch your blogs. Please try again later.";
  }
});
</script>
