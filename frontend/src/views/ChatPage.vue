<template>
  <div class="min-h-screen bg-black text-white flex flex-col">
    <!-- Header -->
    <div class="px-6 text-center py-4 border-b border-gray-700">
      <h1 class="text-2xl font-semibold">Anonymous Chat</h1>
      <p class="text-gray-400 text-sm">You're chatting about: <span class="text-white font-medium">“{{ blogTitle }}”</span></p>
    </div>

    <!-- Chat Window -->
    <div class="flex-1 overflow-y-auto p-6 space-y-4">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="msg.sender === 'me' ? 'text-right' : 'text-left'"
      >
        <div
          :class="msg.sender === 'me'
            ? 'bg-blue-600 text-white ml-auto'
            : 'bg-gray-800 text-white mr-auto'
          "
          class="inline-block max-w-xs px-4 py-2 rounded-xl"
        >
          {{ msg.text }}
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="border-t border-gray-700 p-4">
      <form @submit.prevent="sendMessage" class="flex gap-2">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Type your message..."
          class="flex-1 px-4 py-2 rounded-full bg-gray-900 border border-gray-700 text-white outline-none"
        />
        <button
          type="submit"
          class="px-4 py-2 bg-white text-black rounded-full font-semibold hover:bg-gray-300 transition"
        >
          Send
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const blogTitle = "The Day I Let Go" // example, dynamic later
const newMessage = ref('')
const messages = ref([
  { sender: 'me', text: 'Hey, I loved your blog.' },
  { sender: 'other', text: 'Thank you. I didn’t think anyone would actually read it.' },
])

const sendMessage = () => {
  if (newMessage.value.trim()) {
    messages.value.push({ sender: 'me', text: newMessage.value })
    newMessage.value = ''
  }
}
</script>

<style scoped>
</style>
