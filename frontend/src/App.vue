<template>
  <div class="relative min-h-screen bg-black text-white">
    <!-- ✅ Hamburger Icon -->
    <button
      @click="toggleSidebar"
      class="fixed top-4 left-4 z-50 p-2 bg-white text-black rounded-md hover:bg-gray-200 transition"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        stroke-width="2"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M4 6h16M4 12h16M4 18h16"
        />
      </svg>
    </button>

    <!-- 🔙 Back Arrow -->
    <RouterLink
      v-if="showBackArrow"
      @click.prevent="goBack"
      to="#"
      class="fixed top-4 left-16 z-50 text-white hover:text-gray-300 text-xl"
    >
      ←
    </RouterLink>

    <!-- ✅ Sidebar -->
    <transition name="slide-fade">
      <aside
        v-if="sidebarOpen"
        class="fixed top-0 left-0 h-full w-64 bg-[#0d1117] border-r border-gray-800 pt-20 px-6 z-40"
      >
<h2 class="text-2xl font-bold mb-6"><img src="/logo-removebg-preview.png" class="img-fluid" alt=""></h2>
        <nav class="flex flex-col gap-4">
          <RouterLink to="/" class="hover:underline" @click="closeSidebar"
            >Home</RouterLink
          >
          <RouterLink to="/write" class="hover:underline" @click="closeSidebar"
            >Write</RouterLink
          >
          <RouterLink
            to="/blog-explore"
            class="hover:underline"
            @click="closeSidebar"
            >Explore</RouterLink
          >
          <RouterLink
            to="/profile"
            class="hover:underline"
            @click="closeSidebar"
            >Profile</RouterLink
          >
          <RouterLink
            to="/drafts"
            class="hover:underline"
            @click="closeSidebar"
          >
            Drafts
          </RouterLink>
          <RouterLink to="/chat" class="hover:underline" @click="closeSidebar"
            >Chat</RouterLink
          >
        </nav>
      </aside>
    </transition>

    <!-- ✅ Overlay -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 z-30 bg-black bg-opacity-50"
      @click="closeSidebar"
    ></div>

    <!-- ✅ Page Transitions -->
    <transition name="fade" mode="out-in">
      <router-view />
    </transition>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";

const sidebarOpen = ref(false);
const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value;
};
const closeSidebar = () => {
  sidebarOpen.value = false;
};

// 🔙 Back Arrow Logic
const router = useRouter();
const route = useRoute();
const showBackArrow = ref(false);

const goBack = () => {
  router.back();
};

const checkBackVisibility = () => {
  showBackArrow.value = route.path !== "/";
};

// Watch route changes to update visibility
watch(() => route.path, checkBackVisibility, { immediate: true });
</script>

<style scoped>
/* Sidebar Slide */
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.3s ease;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

/* Page Fade */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Active link underline */
.router-link-exact-active {
  font-weight: 600;
  text-decoration: underline;
}
</style>
