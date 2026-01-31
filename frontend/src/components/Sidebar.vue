<script setup>
import { ref } from 'vue'

const menuItems = [
  { nome: 'Dashboard', icon: '📊' },
  { nome: 'Validação de Arquivos', icon: '📄', alerta: 15 },
  { nome: 'Validação de Dados', icon: '🗂️' },
  { nome: 'Configurações', icon: '⚙️' },
  { nome: 'Serviços', icon: '🛠️' },
  { nome: 'Câmeras', icon: '📹' },
  { nome: 'Leitoras', icon: '💳' },
  { nome: 'Concentrador', icon: '🔌' },
  { nome: 'Monitoria', icon: '🖥️' }
]
</script>

<template>
  <aside class="sidebar">
    <div class="logo">
      <span class="icon">📡</span>
      <span class="text">Analista SP</span>
    </div>

    <nav class="menu">
      <div v-for="item in menuItems" :key="item.nome" class="menu-item">
        <span class="menu-icon">{{ item.icon }}</span>
        <span class="menu-text">{{ item.nome }}</span>
        <span v-if="item.alerta" class="badge-alerta">{{ item.alerta }}</span>
      </div>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 260px;
  height: 100vh;
  background: #ffffff; /* Branco */
  color: #1c2434;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  border-right: 1px solid #e2e8f0;
}

.logo {
  padding: 20px;
  font-size: 1.5rem;
  font-weight: bold;
  color: #3c50e0; /* Azul vibrante */
  border-bottom: 1px solid #f1f5f9;
}

.menu-item {
  padding: 12px 25px;
  color: #64748b; /* Cinza médio */
  transition: all 0.2s;
}

.menu-item:hover {
  background: #f8fafc;
  color: #3c50e0;
}

/* Item selecionado (exemplo) */
.menu-item.active {
  background: #eff4ff;
  color: #3c50e0;
  border-right: 3px solid #3c50e0;
}
</style>