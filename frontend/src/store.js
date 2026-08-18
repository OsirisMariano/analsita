import { reactive, computed } from 'vue'

const API_URL = import.meta.env.VITE_API_URL

export const store = reactive({
  arquivos: [],
  
  carregarArquivos: async () => {
    try {
      const res = await fetch(`${API_URL}/arquivos`)
      const data = await res.json()
      store.arquivos = data.arquivos
    } catch (error) {
      console.error('Erro ao carregar arquivos:', error)
    }
  },
  
  dadosValidacao: {},

  carregarDadosValidacao: async () => {
    try {
      const res = await fetch(`${API_URL}/validacao-dados`)
      const data = await res.json()
      store.dadosValidacao = data
    } catch (error) {
      console.error('Erro ao carregar validação de dados:', error)
    }
  },

  // Contador automático de erros para a Badge
  totalErros: computed(() => {
    return store.arquivos.filter(a => a.status === 'ERRO').length
  }),

  // Contador de erros na Validação de Dados (badge da sidebar)
  totalErrosDados: computed(() => {
    return (store.dadosValidacao.validacoes || []).reduce(
      (acc, v) => acc + v.arquivos.filter(a => a.status !== 'ok').length,
      0
    )
  })
})