<script setup>
import { store } from '../store.js'
// Agora usamos store.arquivos em vez de uma lista local fixa
</script>

<template>
  <div class="validacao-container">
    <div class="header-pagina">
      <h2>📂 Validação de Arquivos</h2>
      <p>Verificação de integridade dos arquivos de configuração do sistema.</p>
    </div>

    <div class="tabela-card">
      <table>
        <thead>
          <tr>
            <th>Arquivo</th>
            <th>Caminho / Detalhes</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="arq in store.arquivos" :key="arq.nome" :class="{ 'linha-erro': arq.status === 'ERRO' }">
            <td class="col-nome">{{ arq.nome }}</td>
            <td class="col-caminho">
              {{ arq.caminho }}
              <span v-if="arq.status === 'OK'" class="check">✓</span>
              <span v-else class="warning">⚠️</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.header-pagina { margin-bottom: 25px; }
.header-pagina h2 { color: #1c2434; margin: 0; }
.header-pagina p { color: #64748b; font-size: 0.9rem; }

.tabela-card {
  background: #ffffff;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background: #f8fafc;
  padding: 15px 20px;
  text-align: left;
  font-size: 0.8rem;
  color: #64748b;
  text-transform: uppercase;
  border-bottom: 1px solid #e2e8f0;
}

td {
  padding: 12px 20px;
  border-bottom: 1px solid #f1f5f9;
  font-size: 0.9rem;
  color: #1c2434;
}

.col-nome { font-weight: 500; width: 30%; }
.col-caminho { font-family: monospace; color: #475569; }

/* Estilo para erro baseado na sua imagem */
.linha-erro {
  background-color: #fee2e2 !important; /* Vermelho claro */
}

.linha-erro td {
  color: #b91c1c; /* Texto vermelho escuro */
}

.check { color: #10b981; margin-left: 8px; font-weight: bold; }
.warning { margin-left: 8px; }

tbody tr:hover:not(.linha-erro) {
  background: #f8fafc;
}
</style>