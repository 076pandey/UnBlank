<template>
  <div class="min-h-screen bg-black text-white flex items-center justify-center px-6">
    <div class="w-full max-w-md bg-gray-900 rounded-2xl shadow-xl p-8">
      <h2 class="text-3xl font-bold mb-6 text-center">Welcome to UnBlank</h2>
      <!-- Email Login -->
      
      <form @submit.prevent="login"> <!-- function name jo neeche script mein hai usi naam se likhna hai --> 
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
          Login
        </button>
      </form>

      <p class="text-center text-sm mt-6 text-gray-400">
        Don’t have an account?
        <RouterLink to="/signup" class="underline text-white hover:text-gray-300">Sign up</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from 'axios';

const router = useRouter();
const email = ref('');
const password = ref('');
const VITE_API_URL = import.meta.env.VITE_API_URL;

const login = async () => {
  try {
    if (!email.value.trim() || !password.value) {
      alert("Please fill in all fields.");
      return;
    }

    const res = await axios.post(`${VITE_API_URL}/login`, {
      email: email.value,
      password: password.value
    });

    if (res.status === 200 && res.data.success) {
      // ✅ Save user_id in localStorage
      localStorage.setItem("user_id", res.data.user_id);

      alert("Login successful!");
      router.push('/profile'); // or wherever you want
    } else {
      alert(res.data.message);
    }
  } catch (error) {
    console.log(error);
    alert('Login failed. Please try again.');
  }
}
</script>


<style scoped>
</style>
