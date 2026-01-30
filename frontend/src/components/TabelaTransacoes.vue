<script setup>
defineProps(['transacoes'])
</script>

<template>
  <div class="tabela-container">
    <table>
      <thead>
        <tr>
          <th>Horário</th>
          <th>Placa</th>
          <th>Valor</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="t in transacoes" :key="t.id">
          <td>{{ new Date(t.timestamp).toLocaleString('pt-BR') }}</td>
          <td class="placa">{{ t.placa }}</td>
          <td>R$ {{ t.valor.toFixed(2) }}</td>
          <td>
            <span class="badge" :class="t.status.toLowerCase()">
              {{ t.status }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.tabela-container {
  background: #2a2a2a;
  border-radius: 8px;
  overflow: hidden;
  margin-top: 15px;
}
table {
  width: 100%;
  border-collapse: collapse;
  color: white;
}
th {
  background: #333;
  text-align: left;
  padding: 12px 15px;
  font-size: 0.85rem;
  color: #888;
  text-transform: uppercase;
}
td {
  padding: 12px 15px;
  border-bottom: 1px solid #383838;
  font-size: 0.9rem;
}
.placa { font-weight: bold; font-family: monospace; }
.badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: bold;
}
.concluido { background: #00bd7e33; color: #00bd7e; }
.falha { background: #ff525233; color: #ff5252; }
</style>