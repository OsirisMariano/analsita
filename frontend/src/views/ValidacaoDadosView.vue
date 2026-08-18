<script setup>
import { reactive, onMounted } from 'vue'
import { store } from '../store'
import { Database, CheckCircle2, XCircle, Files, ChevronDown } from '@lucide/vue'

const aberto = reactive({})

onMounted(async () => {
  await store.carregarDadosValidacao()
  for (const v of store.dadosValidacao.validacoes || []) {
    aberto[v.dado] = false
  }
})

const alternar = (dado) => {
  aberto[dado] = !aberto[dado]
}
</script>

<template>
  <div class="p-4 bg-slate-50 min-h-screen text-sm">

    <!-- Header -->
    <div class="bg-white p-4 rounded-t-lg border border-gray-200 shadow-sm mb-0">
      <div class="flex items-center gap-2">
        <span class="flex items-center justify-center h-10 w-10 rounded-lg bg-primary-light text-primary">
          <Database :size="20" />
        </span>
        <div>
          <h1 class="text-base font-bold text-gray-800 leading-tight">Validação de Dados</h1>
          <p class="text-xs text-gray-500">Verificação dos dados de configuração do sistema.</p>
        </div>
      </div>
    </div>

    <!-- Resumo -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 my-4">
      <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm flex items-center gap-3">
        <span class="text-2xl">{{ store.dadosValidacao.status_geral === 'sucesso' ? '✅' : '❌' }}</span>
        <div>
          <p class="text-xs text-gray-500 uppercase tracking-wider">Status Geral</p>
          <p :class="['font-bold', store.dadosValidacao.status_geral === 'sucesso' ? 'text-green-600' : 'text-red-600']">
            {{ store.dadosValidacao.status_geral }}
          </p>
        </div>
      </div>

      <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm flex items-center gap-3">
        <span class="flex items-center justify-center h-10 w-10 rounded-lg bg-primary-light text-primary">
          <Files :size="20" />
        </span>
        <div>
          <p class="text-xs text-gray-500 uppercase tracking-wider">Arquivos Validados</p>
          <p class="font-bold text-gray-800">{{ store.dadosValidacao.arquivos_validados_total || 0 }}</p>
        </div>
      </div>

      <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm flex items-center gap-3">
        <span class="flex items-center justify-center h-10 w-10 rounded-lg bg-primary-light text-primary">
          <CheckCircle2 :size="20" />
        </span>
        <div>
          <p class="text-xs text-gray-500 uppercase tracking-wider">Validações</p>
          <p class="font-bold text-gray-800">{{ (store.dadosValidacao.validacoes || []).length }}</p>
        </div>
      </div>
    </div>

    <!-- Validações -->
    <div
      v-for="validacao in store.dadosValidacao.validacoes || []"
      :key="validacao.dado"
      class="mb-4"
    >
      <div
        class="bg-white border border-gray-200 rounded-t-lg shadow-sm overflow-hidden"
        :class="validacao.status !== 'ok' ? 'border-red-300' : ''"
      >
        <!-- Cabeçalho da validação -->
        <button
          type="button"
          class="w-full flex flex-wrap items-center gap-x-4 gap-y-2 px-4 py-3 border-b border-gray-200 transition-colors"
          :class="validacao.status !== 'ok' ? 'bg-red-50' : 'bg-gray-50 hover:bg-gray-100'"
          :aria-expanded="aberto[validacao.dado]"
          @click="alternar(validacao.dado)"
        >
          <span class="font-bold text-gray-800">{{ validacao.dado }}</span>
          <span class="text-gray-500 font-mono text-xs bg-white border border-gray-200 rounded px-2 py-0.5">
            {{ validacao.valor }}
          </span>
          <span
            class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wide"
            :class="validacao.status === 'ok'
              ? 'bg-green-100 text-green-700 border border-green-200'
              : 'bg-red-100 text-red-700 border border-red-200'"
          >
            {{ validacao.status === 'ok' ? '✓ ok' : '⚠️ ' + validacao.status }}
          </span>
          <span class="ml-auto text-xs text-gray-500">
            {{ validacao.arquivos.length }} arquivos
          </span>
          <ChevronDown
            :size="18"
            class="text-gray-500 transition-transform duration-300"
            :class="aberto[validacao.dado] ? 'rotate-180' : ''"
          />
        </button>

        <!-- Tabela de arquivos -->
        <Transition name="expand">
        <div
          v-show="aberto[validacao.dado]"
          class="grid transition-[grid-template-rows] duration-300"
          :style="{ gridTemplateRows: aberto[validacao.dado] ? '1fr' : '0fr' }"
        >
          <div class="overflow-hidden">
        <table class="w-full text-left border-collapse table-fixed">
          <thead>
            <tr class="bg-white border-b border-gray-200">
              <th class="w-[52%] px-4 py-2 font-semibold text-gray-600 uppercase text-xs tracking-wider">Arquivo</th>
              <th class="w-[33%] px-4 py-2 font-semibold text-gray-600 uppercase text-xs tracking-wider">Dado</th>
              <th class="w-[15%] px-4 py-2 font-semibold text-gray-600 uppercase text-xs tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr
              v-for="(arq, index) in validacao.arquivos"
              :key="arq.caminho_arquivo + '-' + index"
              :class="arq.status !== 'ok' ? 'bg-red-50' : 'hover:bg-gray-50 transition-colors'"
            >
              <td class="px-4 py-2.5 font-mono text-xs text-gray-700 break-words align-top">{{ arq.caminho_arquivo }}</td>
              <td class="px-4 py-2.5 font-mono text-xs text-gray-500 break-words align-top">{{ arq.dado }}</td>
              <td class="px-4 py-2.5 align-top">
                <span
                  v-if="arq.status === 'ok'"
                  class="flex items-center gap-1 text-green-600 font-bold text-xs"
                >
                  <CheckCircle2 :size="14" /> ok
                </span>
                <span
                  v-else
                  class="flex items-center gap-1 text-red-600 font-bold text-xs"
                >
                  <XCircle :size="14" /> {{ arq.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
          </div>
        </div>
        </Transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
.expand-enter-active,
.expand-leave-active {
  transition: grid-template-rows 0.3s ease;
}
</style>
