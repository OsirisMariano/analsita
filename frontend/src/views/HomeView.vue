<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import DispositivoCard from '../components/DispositivoCard.vue'
import TabelaTransacoes from '../components/TabelaTransacoes.vue' // Novo Import
import { API_URL } from '@/api'
import { useRefresh } from '@/composables/useRefresh'

const resumo = ref(null)
const dispositivos = ref([])
const ultimasTransacoes = ref([]) // Nova variável de estado

// #65 (FR-03): o setInterval dispara a cada 5s independentemente de a
// requisição anterior ter terminado. Se a API demorar mais que 5s (ping dos
// 4 dispositivos, disco lento, DB grande), as chamadas se empilham.
// A guarda abaixo faz a próxima requisição só sair quando a anterior
// terminou — o intervalo de 5s continua valendo no caso normal.
const carregando = ref(false)
let intervalo = null

const carregarDados = async () => {
  // Requisição em voo: não empilha outra por cima.
  if (carregando.value) return
  carregando.value = true

  try {
    // Busca resumo/stats e monitoramento em paralelo
    const [resStats, resMonit] = await Promise.all([
      fetch(`${API_URL}/stats`),
      fetch(`${API_URL}/monitoramento`)
    ])

    const dataStats = await resStats.json()
    const dataMonit = await resMonit.json()

    resumo.value = dataStats

    // Tenta capturar a lista. Se não existir, deixa o array vazio [] para não quebrar o código.
    ultimasTransacoes.value = dataStats.transacoes?.lista_detalhada || []
    dispositivos.value = dataMonit.dispositivos

  } catch (error) {
    console.error("Erro ao integrar com API:", error)
  } finally {
    // Libera a guarda mesmo em caso de erro — senão o polling trava para sempre.
    carregando.value = false
  }
}

onMounted(() => {
  carregarDados()
  intervalo = setInterval(carregarDados, 5000)
})

onUnmounted(() => {
  // Sem isso o timer vaza a cada troca de rota.
  if (intervalo) clearInterval(intervalo)
})

// Botão "Atualizar dados" do cabeçalho (#78). A guarda do #65 continua
// valendo: se já há requisição em voo, carregarDados() não empilha outra.
useRefresh(carregarDados)
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
        <!-- A API devolve a contagem de falhas, mas ela não aparecia na
             tela (#82): o operador via quanto vendeu e quantas deram certo,
             mas nunca quantas falharam. -->
        <p class="falha">Falhas: {{ resumo.transacoes.falhas }}</p>
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
.falha { color: #ff5252; font-weight: bold; }
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