<script setup>
// Exemplo de dados - futuramente virão da sua API/Banco
const cameras = [
  { id: 1, nome: 'Entrada Principal', ip: '192.168.1.20', status: 'ONLINE', url: 'https://via.placeholder.com/400x225?text=Stream+Entrada' },
  { id: 2, nome: 'Saída Pista 01', ip: '192.168.1.21', status: 'ONLINE', url: 'https://via.placeholder.com/400x225?text=Stream+Pista+01' },
  { id: 3, nome: 'VPAR Pista 02', ip: '192.168.1.22', status: 'OFFLINE', url: 'https://via.placeholder.com/400x225?text=Sem+Sinal' }
]
</script>

<template>
  <div class="cameras-container">
    <div class="header-pagina">
      <h2>📹 Monitoramento de Câmeras</h2>
      <p>Visualização em tempo real dos dispositivos VPAR e CFTV.</p>
    </div>

    <div class="mosaico-grid">
      <div v-for="cam in cameras" :key="cam.id" class="camera-card">
        <div class="video-placeholder">
          <img :src="cam.url" :alt="cam.nome">
          <span class="badge-status" :class="cam.status.toLowerCase()">{{ cam.status }}</span>
        </div>
        <div class="info-camera">
          <strong>{{ cam.nome }}</strong>
          <span>{{ cam.ip }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header-pagina { margin-bottom: 25px; }
.header-pagina h2 { margin: 0; color: #1c2434; }
.header-pagina p { color: #64748b; font-size: 0.9rem; }

.mosaico-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.camera-card {
  background: #ffffff;
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.video-placeholder {
  position: relative;
  background: #000;
  aspect-ratio: 16 / 9;
}

.video-placeholder img { width: 100%; height: 100%; object-fit: cover; opacity: 0.8; }

.badge-status {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.65rem;
  font-weight: bold;
  color: white;
}

.badge-status.online { background: #10b981; }
.badge-status.offline { background: #ef4444; }

.info-camera {
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-camera strong { color: #1c2434; font-size: 0.95rem; }
.info-camera span { color: #64748b; font-family: monospace; font-size: 0.85rem; }
</style>