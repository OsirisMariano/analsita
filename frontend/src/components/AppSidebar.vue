<script setup>
import { useRoute } from 'vue-router'
import { store } from '@/store'
import { Radio, LayoutDashboard, Cctv, Rss, FileCheck } from '@lucide/vue'

defineProps({
  colapsada: { type: Boolean, default: false },
  aberta: { type: Boolean, default: false }
})
defineEmits(['fechar'])

const route = useRoute()

const menuPrincipal = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard }
]

const menuOperacao = [
  { to: '/cameras', label: 'Câmeras', icon: Cctv },
  { to: '/leitoras', label: 'Leitoras', icon: Rss },
  { to: '/validacao-arquivos', label: 'Validação de Arquivos', icon: FileCheck, badge: true }
]
</script>

<template>
  <aside
    class="fixed inset-y-0 left-0 z-[9999] flex flex-col w-[260px] bg-sidebar transition-all duration-300"
    :class="[
      aberta ? 'translate-x-0' : '-translate-x-full',
      'lg:translate-x-0',
      colapsada ? 'lg:w-20' : 'lg:w-[260px]'
    ]"
  >
    <!-- Logo -->
    <div
      class="flex items-center gap-3 h-16 px-5 border-b border-white/10 shrink-0"
      :class="colapsada ? 'lg:justify-center lg:px-0' : ''"
    >
      <span class="flex items-center justify-center h-9 w-9 rounded-lg bg-primary text-white shrink-0">
        <Radio :size="20" />
      </span>
      <span class="text-lg font-bold text-white" :class="colapsada ? 'lg:hidden' : ''">
        Analista <span class="text-[#8a99af]">SP</span>
      </span>
    </div>

    <!-- Navegação -->
    <nav class="flex-1 overflow-y-auto py-4 px-3 space-y-6">
      <div>
        <p
          class="px-3 mb-2 text-[10px] font-semibold uppercase tracking-widest text-sidebar-text"
          :class="colapsada ? 'lg:hidden' : ''"
        >
          Principal
        </p>
        <ul class="space-y-1">
          <li v-for="item in menuPrincipal" :key="item.to">
            <RouterLink
              :to="item.to"
              @click="$emit('fechar')"
              class="flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium text-sidebar-text transition-colors"
              :class="[
                colapsada ? 'lg:justify-center lg:px-0' : '',
                route.path === item.to
                  ? 'bg-primary text-white'
                  : 'hover:bg-sidebar-hover hover:text-white'
              ]"
            >
              <component :is="item.icon" :size="18" class="shrink-0" />
              <span :class="colapsada ? 'lg:hidden' : ''">{{ item.label }}</span>
            </RouterLink>
          </li>
        </ul>
      </div>

      <div>
        <p
          class="px-3 mb-2 text-[10px] font-semibold uppercase tracking-widest text-sidebar-text"
          :class="colapsada ? 'lg:hidden' : ''"
        >
          Operação
        </p>
        <ul class="space-y-1">
          <li v-for="item in menuOperacao" :key="item.to">
            <RouterLink
              :to="item.to"
              @click="$emit('fechar')"
              class="flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium text-sidebar-text transition-colors"
              :class="[
                colapsada ? 'lg:justify-center lg:px-0' : '',
                route.path === item.to
                  ? 'bg-primary text-white'
                  : 'hover:bg-sidebar-hover hover:text-white'
              ]"
            >
              <component :is="item.icon" :size="18" class="shrink-0" />
              <span class="flex-1" :class="colapsada ? 'lg:hidden' : ''">{{ item.label }}</span>
              <span
                v-if="item.badge && store.totalErros > 0"
                class="rounded-full bg-danger text-white font-bold"
                :class="[
                  colapsada
                    ? 'lg:h-2 lg:w-2 lg:text-[0] lg:ml-0'
                    : 'px-2 py-0.5 text-[10px]'
                ]"
              >
                {{ store.totalErros }}
              </span>
            </RouterLink>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Rodapé -->
    <div
      class="px-5 py-4 border-t border-white/10 text-xs text-sidebar-text shrink-0"
      :class="colapsada ? 'lg:px-0 lg:text-center' : ''"
    >
      <span :class="colapsada ? 'lg:hidden' : ''">v1.0.0 · MVP</span>
      <span class="hidden" :class="colapsada ? 'lg:inline' : ''">v1</span>
    </div>
  </aside>
</template>
