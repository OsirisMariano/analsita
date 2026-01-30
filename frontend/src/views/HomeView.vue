<script setup>
import { ref, onMounted } from 'vue'
import DispositivoCard from '../components/DispositivoCard.vue'

const resumo = ref(null)
const dispositivos = ref([])

const carregarDados = async () => {
  try {
    // Busca os dados globais (vendas/equipamentos totais)
    const resStats = await fetch('http://localhost:8000/stats')
    resumo.value = await resStats.json()

    // Busca o status individual de cada antena/dispositivo
    const resMonit = await fetch('http://localhost:8000/monitoramento')
    const dataMonit = await resMonit.json()
    dispositivos.value = dataMonit.dispositivos
  } catch (error) {
    console.error("Erro ao integrar com API:", error)
  }
}

onMounted(() => {
  carregarDados()
  setInterval(carregarDados, 5000) // Atualiza a cada 5 segundos
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
  </main>
</template>

<style scoped>
.stats-container {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}
.card {
  background: #2a2a2a;
  padding: 20px;
  border-radius: 8px;
  flex: 1;
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