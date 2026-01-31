<script setup>
import { store } from '../store' // Importando seu store centralizado

// Dados das antenas (podem ser movidos para o store.js depois)
const antenas = [
  { nome: 'Antena Lado A', ip: '192.168.1.10', status: 'CONCLUIDO', ultimaLeitura: 'Há 2 minutos' },
  { nome: 'Antena Lado B', ip: '192.168.1.11', status: 'EM_ABERTO', ultimaLeitura: '-' }
]

const reiniciarAntena = (nome) => {
  alert(`Comando de reinício enviado para: ${nome}`)
}
</script>

<template>
  <div class="p-4 bg-slate-50 min-h-screen text-sm">
    
    <div class="bg-white p-4 rounded-t-lg border border-gray-200 shadow-sm mb-0">
      <div class="flex items-center gap-2">
        <span class="text-xl">📡</span>
        <div>
          <h1 class="text-base font-bold text-gray-800 leading-tight">Monitoramento de Leitoras</h1>
          <p class="text-xs text-gray-500">Verificação de integridade e status das antenas de pista.</p>
        </div>
      </div>
    </div>

    <div class="bg-white border-x border-b border-gray-200 rounded-b-lg shadow-sm overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="px-4 py-3 font-semibold text-gray-600 uppercase text-xs tracking-wider">Dispositivo</th>
            <th class="px-4 py-3 font-semibold text-gray-600 uppercase text-xs tracking-wider">IP</th>
            <th class="px-4 py-3 font-semibold text-gray-600 uppercase text-xs tracking-wider">Status</th>
            <th class="px-4 py-3 font-semibold text-gray-600 uppercase text-xs tracking-wider">Última Leitura</th>
            <th class="px-4 py-3 font-semibold text-gray-600 uppercase text-xs tracking-wider text-center">Ações</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="antena in antenas" :key="antena.ip" class="hover:bg-gray-50 transition-colors">
            <td class="px-4 py-3 font-bold text-blue-900 italic">{{ antena.nome }}</td>
            <td class="px-4 py-3 text-gray-600 font-mono text-xs">{{ antena.ip }}</td>
            <td class="px-4 py-3">
              <span :class="[
                'px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wide',
                antena.status === 'CONCLUIDO' ? 'bg-green-100 text-green-700 border border-green-200' : 'bg-amber-100 text-amber-700 border border-amber-200'
              ]">
                {{ antena.status }}
              </span>
            </td>
            <td class="px-4 py-3 text-gray-500">{{ antena.ultimaLeitura }}</td>
            <td class="px-4 py-3 text-center">
              <button 
                @click="reiniciarAntena(antena.nome)"
                class="inline-flex items-center gap-1 px-3 py-1 bg-white border border-gray-300 text-gray-700 text-[10px] font-black rounded hover:bg-orange-50 hover:text-orange-600 hover:border-orange-200 transition-all active:scale-90 shadow-sm"
              >
                REINICIAR
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>