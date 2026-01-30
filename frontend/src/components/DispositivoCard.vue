<script setup>
defineProps(['dispositivo'])
</script>

<template>
  <div class="card-dispositivo" :class="dispositivo.status.toLowerCase()">
    <div class="header">
      <span class="status-icon"></span>
      <h4>{{ dispositivo.nome }}</h4>
    </div>
    <div class="info">
      <p class="ip">{{ dispositivo.ip }}</p>
      <p class="status-text">{{ dispositivo.status }}</p>
    </div>
  </div>
</template>

<style scoped>
.card-dispositivo {
  background: #2a2a2a;
  border-radius: 8px;
  padding: 15px;
  border-left: 4px solid #555;
}
.card-dispositivo.online { border-left-color: #00bd7e; }
.card-dispositivo.offline { border-left-color: #ff5252; }

.header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.status-icon { width: 10px; height: 10px; border-radius: 50%; background: #555; }
.online .status-icon { background: #00bd7e; box-shadow: 0 0 8px #00bd7e; }
.offline .status-icon { background: #ff5252; }

h4 { margin: 0; color: white; }
.ip { font-family: monospace; color: #888; margin: 5px 0; font-size: 0.9rem; }
.status-text { font-weight: bold; font-size: 0.75rem; text-transform: uppercase; }
</style>