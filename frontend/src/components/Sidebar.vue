<script setup>
import { store } from '@/store';
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
      <RouterLink to="/" class="menu-item" active-class="active">
        <span class="menu-icon">📊</span>
        <span class="menu-text">Dashboard</span>
      </RouterLink>

      <RouterLink to="/cameras" class="menu-item" active-class="active">
        <span class="menu-icon">📹</span>
        <span class="menu-text">Câmeras</span>
      </RouterLink>
      
      <RouterLink to="/leitoras" class="menu-item" active-class="active">
        <span class="menu-icon">📡</span>
        <span class="menu-text">Leitoras</span>
      </RouterLink>

      <RouterLink to="/validacao-arquivos" class="menu-item" active-class="active">
        <span class="menu-icon">📄</span>
        <span class="menu-text">Validação de Arquivos</span>
        <span v-if="store.totalErros > 0" class="badge-alerta">
          {{ store.totalErros }}
        </span>
      </RouterLink>
    </nav>
  </aside>
</template>

<style scoped>
.sidebar {
  /* Fixa a barra na lateral esquerda */
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 260px;
  
  /* Cores e Bordas */
  background-color: #ffffff;
  border-right: 1px solid #e2e8f0;
  
  /* Alinhamento interno */
  display: flex;
  flex-direction: column;
  z-index: 9999; /* Garante que fique acima de tudo */
}

.logo {
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 700;
  font-size: 1.25rem;
  color: #1c2434;
  border-bottom: 1px solid #f1f5f9;
}

.menu {
  flex: 1;
  padding: 16px 0;
  display: flex;
  flex-direction: column;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  color: #64748b;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
}

.menu-item:hover {
  background-color: #f8fafc;
  color: #3c50e0;
}

/* Estilo para o link ativo (onde você está no momento) */
.active {
  background-color: #eff4ff;
  color: #3c50e0;
  border-right: 4px solid #3c50e0;
}

.badge-alerta {
  margin-left: auto;
  background: #eb5757;
  color: white;
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 10px;
}
</style>