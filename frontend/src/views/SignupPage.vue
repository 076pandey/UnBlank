<template>
  <div
    class="min-h-screen bg-black text-white flex items-center justify-center px-6"
  >
    <div class="w-full max-w-md bg-gray-900 rounded-2xl shadow-xl p-8">
      <h2 class="text-3xl font-bold mb-6 text-center">Create Your Account</h2>

      <form @submit.prevent="signup">
        <!-- function name jo neeche script mein hai usi naam se likhna hai -->
        <input
          v-model="username"
          type="text"
          placeholder="Username"
          class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 mb-4 outline-none placeholder-gray-400"
        />
        <input
          v-model="email"
          type="email"
          placeholder="Email"
          class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 mb-4 outline-none placeholder-gray-400"
        />
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 mb-6 outline-none placeholder-gray-400"
        />
        <button
          class="w-full bg-white text-black font-semibold py-3 rounded-full hover:bg-gray-200 transition"
        >
          Sign Up
        </button>
      </form>

      <p class="text-center text-sm mt-6 text-gray-400">
        Already have an account?
        <RouterLink to="/login" class="underline text-white hover:text-gray-300"
          >Log in</RouterLink
        >
      </p>
    </div>
  </div>
</template>
<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const username = ref("");
const email = ref("");
const password = ref("");
const VITE_API_URL = import.meta.env.VITE_API_URL;

const signup = async () => {
  if (!username.value.trim() || !email.value.trim() || !password.value) {
    alert("Please fill in all fields.");
    return;
  }

  try {
    const res = await axios.post(`${VITE_API_URL}/signup`, {
      username: username.value.trim(),
      email: email.value.trim().toLowerCase(),
      password: password.value,
    });

    // ✅ Store data (if needed) and redirect
    if (res.status === 200) {
      const { user_id, username: returnedUsername } = res.data;

      // Optional: store user info
      localStorage.setItem("user_id", user_id);
      localStorage.setItem("username", returnedUsername);

      alert("Signup successful!");
      router.push("/write");
    }
  } catch (error) {
    // ✅ Fix here
    if (error.response && error.response.data && error.response.data.error) {
      alert(error.response.data.error);
    } else {
      alert("An unexpected error occurred. Please try again later.");
    }
  }
};
</script>

<style scoped></style>
