<script setup>
import { store } from '../store' 
</script>

<template>
  <div class="p-4 bg-slate-50 min-h-screen text-sm">
    
    <div class="bg-white p-4 rounded-t-lg border border-gray-200 shadow-sm mb-0">
      <div class="flex items-center gap-2">
        <span class="text-xl">📂</span>
        <div>
          <h1 class="text-base font-bold text-gray-800 leading-tight">Validação de Arquivos</h1>
          <p class="text-xs text-gray-500">Verificação de integridade dos arquivos de configuração do sistema.</p>
        </div>
      </div>
    </div>

    <div class="bg-white border-x border-b border-gray-200 rounded-b-lg shadow-sm overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-4 py-3 font-semibold text-gray-600 uppercase text-xs tracking-wider">Arquivo</th>
            <th class="px-4 py-3 font-semibold text-gray-600 uppercase text-xs tracking-wider">Caminho / Detalhes</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="arq in store.arquivos" 
              :key="arq.nome" 
              :class="[arq.status === 'ERRO' ? 'bg-red-50' : 'hover:bg-gray-50 transition-colors']">
            <td class="px-4 py-3 font-medium text-gray-900">{{ arq.nome }}</td>
            <td class="px-4 py-3 text-gray-600 flex items-center justify-between">
              <span>'{{ arq.caminho }}'</span>
              <span v-if="arq.status === 'OK'" class="text-green-500 font-bold ml-2">✓</span>
              <span v-else class="text-yellow-500 text-lg ml-2">⚠️</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
/* Removido o CSS antigo para usar Tailwind e garantir o Light Mode */
</style>