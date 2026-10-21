import { onMounted, onUnmounted } from 'vue'

// O botão "Atualizar dados" do cabeçalho (App.vue) dispara um evento no
// window; quem tem dado vivo escuta por ele (#78). O removeEventListener
// no onUnmounted é obrigatório: sem ele, cada ida e volta entre as telas
// vaza um listener e o evento passa a disparar N vezes.
export function useRefresh(callback) {
  const aoSolicitarRefresh = () => callback()

  onMounted(() => {
    window.addEventListener('analista:refresh', aoSolicitarRefresh)
  })

  onUnmounted(() => {
    window.removeEventListener('analista:refresh', aoSolicitarRefresh)
  })
}
