<script setup>
import { ref, onMounted } from 'vue'

const resumo = ref(null)

const carregarDados = async () => {
  try {
    const response = await fetch('http://localhost:8000/stats')
    resumo.value = await response.json()
  } catch (error) {
    console.error("Erro ao buscar dados da API:", error)
  }
}

onMounted(() => {
  carregarDados()
  // Atualiza a cada 5 segundos para simular monitoramento em tempo real
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
    <div v-else>Carregando dados da pista...</div>
  </main>
</template>

<style scoped>
.stats-container {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}
.card {
  background: #2a2a2a;
  padding: 20px;
  border-radius: 8px;
  border-left: 5px solid #00bd7e;
  flex: 1;
}
.online { color: #00bd7e; font-weight: bold; }
.offline { color: #ff5252; font-weight: bold; }
.valor { font-size: 24px; color: #ffd700; }
</style>