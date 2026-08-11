<template>
  <div class="min-h-screen bg-body">
    <AppSidebar
      :colapsada="sidebarColapsada"
      :aberta="menuAberto"
      @fechar="menuAberto = false"
    />

    <!-- Backdrop mobile -->
    <div
      v-if="menuAberto"
      class="fixed inset-0 z-[9998] bg-black/50 lg:hidden"
      @click="menuAberto = false"
    ></div>

    <div
      class="flex flex-col min-h-screen transition-[margin] duration-300"
      :class="sidebarColapsada ? 'lg:ml-20' : 'lg:ml-[260px]'"
    >
      <!-- Header -->
      <header class="sticky top-0 z-[999] h-16 bg-white border-b border-border flex items-center gap-4 px-4 lg:px-8 shadow-sm">
        <button
          class="flex items-center justify-center h-10 w-10 rounded-lg text-text-secondary hover:bg-slate-100 hover:text-text lg:hidden"
          @click="menuAberto = true"
          title="Abrir menu"
        >
          <Menu :size="22" />
        </button>

        <button
          class="hidden lg:flex items-center justify-center h-10 w-10 rounded-lg text-text-secondary hover:bg-slate-100 hover:text-text"
          @click="sidebarColapsada = !sidebarColapsada"
          :title="sidebarColapsada ? 'Expandir menu' : 'Recolher menu'"
        >
          <PanelLeftClose v-if="!sidebarColapsada" :size="20" />
          <PanelLeftOpen v-else :size="20" />
        </button>

        <div class="flex-1 min-w-0">
          <p class="text-xs font-medium text-text-secondary">
            <span class="uppercase tracking-widest">Sistema</span>
            <span class="mx-1.5 text-slate-300">/</span>
            <span class="text-primary">Monitoramento</span>
          </p>
        </div>

        <div class="flex items-center gap-3">
          <span class="hidden sm:inline text-sm font-medium text-text-secondary tabular-nums">
            {{ horaAtual }}
          </span>

          <button
            class="flex items-center justify-center h-10 w-10 rounded-lg text-text-secondary hover:bg-slate-100 hover:text-primary"
            title="Atualizar dados"
            @click="solicitarRefresh"
          >
            <RefreshCw :size="18" />
          </button>

          <div class="h-9 w-9 rounded-full bg-primary text-white flex items-center justify-center text-sm font-bold select-none">
            AS
          </div>
        </div>
      </header>

      <!-- Conteúdo -->
      <main class="flex-1 p-4 lg:p-8">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { RouterView } from 'vue-router'
import { Menu, PanelLeftClose, PanelLeftOpen, RefreshCw } from '@lucide/vue'
import AppSidebar from './components/AppSidebar.vue'

const menuAberto = ref(false)
const sidebarColapsada = ref(false)
const horaAtual = ref('')
let timer

const atualizarHora = () => {
  horaAtual.value = new Date().toLocaleTimeString('pt-BR')
}

const solicitarRefresh = () => {
  window.dispatchEvent(new Event('analista:refresh'))
}

onMounted(() => {
  atualizarHora()
  timer = setInterval(atualizarHora, 1000)
})

onBeforeUnmount(() => {
  clearInterval(timer)
})
</script>

<style>
/* Reset radical para matar qualquer CSS fantasma */
body, html, #app {
  margin: 0 !important;
  padding: 0 !important;
  height: 100% !important;
}
</style>
