<template>
  <div class="flex min-h-screen w-full bg-slate-50">
    <aside class="w-[260px] flex-shrink-0">
      <Sidebar />
    </aside>

    <div class="flex-1 flex flex-col min-w-0 h-screen overflow-hidden">
      
      <header class="h-16 bg-white border-b border-gray-200 flex items-center px-8 shadow-sm">
        <h2 class="text-sm font-medium text-gray-500 uppercase tracking-widest">
          Sistema / <span class="text-blue-600">Monitoramento</span>
        </h2>
      </header>

      <main class="flex-1 overflow-y-auto p-6 bg-slate-50">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
</script>

<style>
/* Reset radical para matar qualquer CSS fantasma */
body, html, #app {
  margin: 0 !important;
  padding: 0 !important;
  height: 100% !important;
}
</style>