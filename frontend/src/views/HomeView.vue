<script setup>
import { ref, onMounted } from 'vue'
import DispositivoCard from '../components/DispositivoCard.vue'
import TabelaTransacoes from '../components/TabelaTransacoes.vue' // Novo Import

const resumo = ref(null)
const dispositivos = ref([])
const ultimasTransacoes = ref([]) // Nova variável de estado

const carregarDados = async () => {
  try {
    // Busca resumo/stats e monitoramento em paralelo
    const [resStats, resMonit] = await Promise.all([
      fetch(`${import.meta.env.VITE_API_URL}/stats`),
      fetch(`${import.meta.env.VITE_API_URL}/monitoramento`)
    ])

    const dataStats = await resStats.json()
    const dataMonit = await resMonit.json()

    resumo.value = dataStats

    // Tenta capturar a lista. Se não existir, deixa o array vazio [] para não quebrar o código.
    ultimasTransacoes.value = dataStats.transacoes?.lista_detalhada || []
    dispositivos.value = dataMonit.dispositivos

  } catch (error) {
    console.error("Erro ao integrar com API:", error)
  }
}

onMounted(() => {
  carregarDados()
  setInterval(carregarDados, 5000)
})
</script>

<template>
  <main>
    <div v-if="resumo" class="stats-container">
      <div class="card">
        <h3>Equipamentos</h3>
        <p>Online: <span class="online">{{ resumo.monitoramento.online }}</span></p>
        <p>Offline: <span class="offline">{{ resumo.monitoramento.offline }}</span></p>
      </div>

      <div class="card">
        <h3>Vendas Hoje</h3>
        <p class="valor">R$ {{ resumo.transacoes.valor_total }}</p>
        <p>Sucesso: {{ resumo.transacoes.concluidas }}</p>
      </div>
    </div>

    <h2 class="section-title">📡 Saúde da Pista (Status Individual)</h2>
    <div class="grid-dispositivos">
      <DispositivoCard 
        v-for="item in dispositivos" 
        :key="item.ip" 
        :dispositivo="item" 
      />
    </div>

    <h2 class="section-title">💸 Últimas Transações (Tempo Real)</h2>
    <TabelaTransacoes :transacoes="ultimasTransacoes" />
    
  </main>
</template>

<style scoped>
.stats-container {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}
.card {
  background: #fff !important;
  padding: 20px;
  border-radius: 15px;
  border: 1px solid #e2e8f0;
  flex: 1;
}

h2, h3 .section-title {
  color: #1c2434 !important;
}

.online { color: #00bd7e; font-weight: bold; }
.offline { color: #ff5252; font-weight: bold; }
.valor { font-size: 24px; color: #ffd700; }

.section-title {
  margin-top: 40px;
  color: #888;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.grid-dispositivos {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 15px;
  margin-top: 15px;
}
</style>