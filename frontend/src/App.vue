<script setup>
import { RouterView } from 'vue-router'
import Sidebar from './components/Sidebar.vue' // Importando o novo menu
</script>

<template>
  <div class="app-layout">
    <Sidebar />

    <div class="main-content">
      <header class="top-bar">
        <span>Monitoramento de Pista / <strong>Dashboard</strong></span>
      </header>
      
      <div class="view-container">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<style>
body, html {
  margin: 0;
  padding: 0;
  font-family: 'Inter', sans-serif;
  background-color: #f1f5f9; 
  color: #1c2434;
}

h1, h2, h3, h4 {
 font-weight: 600;
 color: #1c2434;
} 

.main-content {
  flex: 1;
  margin-left: 260px; 
  display: flex;
  flex-direction: column;
}

.top-bar {
  background: #ffffff; /* Branco total */
  color: #64748b;
  padding: 15px 30px;
  border-bottom: 1px solid #e2e8f0;
  font-size: 0.9rem;
}

.view-container {
  padding: 20px 30px;
}
</style>