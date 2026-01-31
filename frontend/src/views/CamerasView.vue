<script setup>
// Exemplo de dados mantido conforme o original
const cameras = [
  { id: 1, nome: 'Entrada Principal', ip: '192.168.1.20', status: 'ONLINE', url: 'https://via.placeholder.com/400x225?text=Stream+Entrada' },
  { id: 2, nome: 'Saída Pista 01', ip: '192.168.1.21', status: 'ONLINE', url: 'https://via.placeholder.com/400x225?text=Stream+Pista+01' },
  { id: 3, nome: 'VPAR Pista 02', ip: '192.168.1.22', status: 'OFFLINE', url: 'https://via.placeholder.com/400x225?text=Sem+Sinal' }
]
</script>

<template>
  <div class="p-4 bg-slate-50 min-h-screen">
    
    <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm mb-6">
      <div class="flex items-center gap-2">
        <span class="text-xl">📹</span>
        <div>
          <h1 class="text-base font-bold text-gray-800 leading-tight">Monitoramento de Câmeras</h1>
          <p class="text-xs text-gray-500">Visualização em tempo real dos dispositivos VPAR e CFTV.</p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="cam in cameras" :key="cam.id" 
           class="bg-white rounded-xl overflow-hidden border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
        
        <div class="relative bg-black aspect-video group">
          <img :src="cam.url" :alt="cam.nome" class="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity">
          
          <span :class="[
            'absolute top-3 right-3 px-2 py-1 rounded text-[10px] font-bold text-white tracking-wider',
            cam.status === 'ONLINE' ? 'bg-emerald-500' : 'bg-red-500'
          ]">
            {{ cam.status }}
          </span>
        </div>

        <div class="p-4 flex justify-between items-center">
          <span class="text-sm font-bold text-gray-800">{{ cam.nome }}</span>
          <span class="text-xs font-mono text-gray-500 bg-gray-50 px-2 py-1 rounded border border-gray-100">
            {{ cam.ip }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Nenhum CSS necessário - tudo controlado por classes Tailwind */
</style>