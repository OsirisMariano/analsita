<script setup>
defineProps(['dispositivo'])
</script>

<template>
  <div class="card">
    <div class="status-indicator" :class="dispositivo.status.toLowerCase()"></div>
    <div class="card-content">
      <h3>{{ dispositivo.nome }}</h3>
      <p class="ip">{{ dispositivo.ip }}</p>
      <span class="status-text" :class="dispositivo.status.toLowerCase()">
        {{ dispositivo.status }}
      </span>
    </div>
  </div>
</template>

<style scoped>
.card {
  background: #ffffff; /* Fundo Branco */
  border-radius: 10px;
  padding: 20px;
  display: flex;
  gap: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); /* Sombra suave */
  border: 1px solid #e2e8f0;
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 5px;
}

.status-indicator.online { background-color: #10b981; }
.status-indicator.offline { background-color: #ef4444; }

h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #1c2434;
}

.ip {
  margin: 5px 0;
  color: #64748b;
  font-family: monospace;
}

.status-text {
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
}

.status-text.online { color: #10b981; }
.status-text.offline { color: #ef4444; }
</style>