<script setup>
defineProps(['transacoes'])
</script>

<template>
  <div class="tabela-container">
    <table>
      <thead>
        <tr>
          <th>Horário</th>
          <th>Placa (Tag)</th>
          <th>Valor</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="t in transacoes" :key="t.id">
          <td class="timestamp">{{ new Date(t.timestamp).toLocaleString('pt-BR') }}</td>
          <td class="placa">{{ t.veiculo_tag || '---' }}</td>
          <td class="valor">R$ {{ t.valor.toFixed(2) }}</td>
          <td>
            <span class="badge" :class="t.status.toLowerCase().replace('_', '-')">
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
  background: #ffffff;
  border-radius: 10px;
  overflow: hidden;
  margin-top: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background: #f8fafc;
  text-align: left;
  padding: 15px;
  font-size: 0.8rem;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #e2e8f0;
}

td {
  padding: 14px 15px;
  border-bottom: 1px solid #f1f5f9;
  font-size: 0.95rem;
  color: #1c2434;
}

tbody tr:nth-child(even) {
  background: #fbfcfd; /* Linha zebra clara */
}

tbody tr:hover {
  background: #f1f5f9;
}

.timestamp { color: #64748b; }

.placa { 
  font-weight: bold; 
  font-family: 'Courier New', Courier, monospace; 
  color: #3c50e0; /* Azul vibrante */
}

.valor { font-weight: 600; }

.badge {
  padding: 5px 12px;
  border-radius: 50px;
  font-size: 0.7rem;
  font-weight: 800;
  display: inline-block;
  min-width: 100px;
  text-align: center;
}

/* Cores das Badges no Light Mode */
.concluido { 
  background: #e1f9f0; 
  color: #10b981; 
}

.em-aberto { 
  background: #fff4e5; 
  color: #ffab00; 
}

.falha { 
  background: #fee2e2; 
  color: #ef4444; 
}
</style>