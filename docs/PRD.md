# PRD — Analista SemParar

**Product Requirements Document**

| Campo | Detalhe |
|---|---|
| **Produto** | Analista SemParar |
| **Versão do documento** | 1.0 |
| **Status** | Em desenvolvimento (V1 em andamento) |
| **Data** | 10/08/2026 |
| **Autor** | Equipe de Desenvolvimento |
| **Stack** | Python/FastAPI, Vue 3, Tailwind CSS, SQLite, Docker |

---

## 1. Sumário Executivo

O Analista SemParar é um painel (dashboard) de monitoramento de infraestrutura de pista para o sistema de abastecimento SemParar. Ele transforma a lógica de diagnóstico baseada em terminal — leitura manual de logs e comandos `ping` — em uma interface visual moderna, permitindo a **identificação proativa de falhas** e a **redução do tempo de diagnóstico** pelo suporte técnico operacional.

A **V1 (MVP)** centraliza os dados críticos coletados pelo motor de análise em indicadores visuais de fácil leitura.

## 2. Problema & Contexto

### 2.1 Contexto atual
- O diagnóstico de falhas em pistas (antenas, sensores, VPAR) é feito manualmente por terminal: comandos de `ping`, leitura de arquivos de configuração (`posto.json`, `concentrador.json`, `sensor.json`, etc.) e checagem de licenças.
- Os dados de transações ficam isolados em banco SQLite local, sem agregação visual.
- Não há visão centralizada do status de conectividade dos equipamentos.

### 2.2 Problemas observados
1. **Alto tempo de diagnóstico (MTTR alto):** o analista precisa executar múltiplos comandos e correlacionar resultados manualmente.
2. **Dependência de conhecimento técnico:** a interpretação de logs varia entre analistas (conhecimento tribal).
3. **Falhas detectadas de forma reativa:** o problema só é percebido quando o posto reporta.
4. **Sem histórico nem alertas:** não há acúmulo de dados para análise de recorrência.

### 2.3 Proposta de valor
- **Centralizar** em uma única tela o status de conectividade, transações e integridade de arquivos.
- **Visualizar** em tempo real (Online/Offline) cada dispositivo da pista.
- **Automatizar** a checagem de arquivos e licenças que hoje é manual.
- **Prover alertas** de saúde do sistema (backlog V2).

## 3. Público-alvo & Personas

### Persona primária — Analista de Suporte Operacional
- **Perfil:** técnico de suporte de campo/remoto que atende chamados de postos.
- **Necessidade:** identificar rapidamente se a falha é de conectividade, software (VPAR/licença) ou hardware.
- **Contexto:** usa terminal e acesso ao posto; quer um painel que resuma o estado antes de intervir.

### Persona secundária — Supervisor / NOC
- **Perfil:** coordena equipes e acompanha saúde da frota de postos.
- **Necessidade:** visão agregada de online/offline e vendas por período.
- **Contexto:** consome o dashboard para priorizar chamados.

### Fora do público da V1
- Operadores de caixa/posto (sem necessidade de diagnóstico).
- Clientes finais.

## 4. Objetivos & Métricas de Sucesso

### 4.1 Objetivos do produto (V1)
| # | Objetivo |
|---|---|
| O1 | Reduzir o tempo de diagnóstico de falhas em pista (MTTR). |
| O2 | Centralizar dados críticos (conectividade, transações, arquivos) em uma interface. |
| O3 | Detectar problemas de configuração (arquivos/licença) sem acesso manual ao terminal. |
| O4 | Estabelecer base técnica (API + dashboard + Docker) para evolução futura. |

### 4.2 Métricas de sucesso
| Métrica | Meta da V1 | Como medir |
|---|---|---|
| Tempo para identificar causa raiz | Redução ≥ 50% vs. fluxo manual | Time de suporte |
| Ferramentas/sessões por chamado | 1 dashboard (vs. N comandos) | Adoção da ferramenta |
| Visibilidade de falhas proativas | ≥ 1 alerta visual por turno | Uso do dashboard |
| Disponibilidade do painel | ≥ 99% | Uptime do serviço |

> Métricas de impacto financeiro (ex.: perda de receita por pista parada) devem ser definidas com o negócio.

## 5. Escopo da V1 (MVP)

### 5.1 Incluído na V1

| Módulo | Descrição | Status |
|---|---|---|
| Dashboard | Resumo agregado: equipamentos online/offline, vendas do dia, sucesso/falhas | ✅ Entregue |
| Monitoramento de conectividade | Ping em tempo real das antenas, VPAR e saída de internet | ✅ Entregue |
| Transações em tempo real | Tabela com as últimas transações lidas do SQLite (atualização periódica) | ✅ Entregue |
| Validação de arquivos | Tabela de arquivos de configuração com status OK/ERRO e badge de alerta | ✅ Entregue |
| Página de Câmeras | Grid de visualização de streams VPAR/CFTV | ✅ Entregue (dados mockados) |
| Página de Leitoras | Status das antenas + ação de reinício | ✅ Entregue (dados mockados) |
| Simulador de dados | Script para gerar banco SQLite com transações de teste | ✅ Entregue |
| Infraestrutura | Docker Compose com API + frontend e montagem do banco | ✅ Entregue |

### 5.2 Fora do escopo da V1
- Autenticação e controle de acesso (usuários/roles).
- Alertas ativos (notificações, integração com WhatsApp/e-mail).
- Histórico persistente e séries temporais de status.
- Integração real com os equipamentos (hoje os IPs são fixos/`hardcoded`).
- Comandos de reinício reais em leitoras (atualmente simulado).
- API de configuração dinâmica de dispositivos.

## 6. Requisitos Funcionais (V1)

> Convenção: `FR-XX` = Requisito Funcional. Cobertura mapeada para os artefatos existentes.

### 6.1 Dashboard
- **FR-01** — O sistema deve exibir o resumo agregado de dispositivos: total, online e offline. *(Backend: `GET /stats` → `monitoramento`; Frontend: `HomeView.vue`)*
- **FR-02** — O sistema deve exibir o total de vendas do dia (soma de `valor` das transações `CONCLUIDO`) e a contagem de sucesso/falhas. *(Backend: `GET /stats` → `transacoes`; Frontend: `HomeView.vue`)*
- **FR-03** — O dashboard deve atualizar os dados automaticamente a cada **5 segundos** (polling). *(Frontend: `HomeView.vue` → `setInterval`)*

### 6.2 Monitoramento de conectividade
- **FR-04** — O sistema deve executar `ping` (1 pacote, timeout 1s) para cada dispositivo cadastrado e retornar status `Online`/`Offline`. *(Backend: `disparar_ping()`)*
- **FR-05** — A lista de dispositivos monitorados deve conter: Antena Lado A, Antena Lado B, Câmera VPAR e Saída Internet. *(Backend: `EQUIPAMENTOS`)*
- **FR-06** — O frontend deve exibir um card individual por dispositivo com indicador visual de status (bolinha colorida + texto). *(Frontend: `DispositivoCard.vue`)*
- **FR-07** — O endpoint `/monitoramento` deve retornar nome, IP e status de cada dispositivo. *(Backend: `GET /monitoramento`)*

### 6.3 Transações em tempo real
- **FR-08** — O sistema deve listar as transações do SQLite ordenadas por `timestamp` decrescente. *(Backend: `GET /transacoes`)*
- **FR-09** — O dashboard deve exibir as **5 últimas transações** com horário, tag/placa, valor e status estilizado. *(Backend: `GET /stats` → `lista_detalhada`; Frontend: `TabelaTransacoes.vue`)*
- **FR-10** — O status da transação deve exibir cores distintas: `CONCLUIDO` (verde), `EM_ABERTO` (âmbar), `FALHA` (vermelho). *(Frontend: `TabelaTransacoes.vue`)*

### 6.4 Validação de arquivos
- **FR-11** — O sistema deve listar os arquivos de configuração críticos do posto (ex.: `posto.json`, `concentrador.json`, `sensor.json`, `ifadapter.ini`, licença VPAR, certificado P12, `zabbix_agent2.conf`, `config.json`). *(Frontend: `store.js`)*
- **FR-12** — Cada arquivo deve exibir status `OK`/`ERRO` com indicador visual. *(Frontend: `ValidacaoArquivosView.vue`)*
- **FR-13** — A sidebar deve exibir um **badge com a contagem de erros** no menu de Validação de Arquivos. *(Frontend: `Sidebar.vue` + `store.totalErros`)*

### 6.5 Câmeras
- **FR-14** — O sistema deve exibir um grid de câmeras com nome, IP e status (ONLINE/OFFLINE). *(Frontend: `CamerasView.vue` — dados mockados)*
- **FR-15** — Cada card de câmera deve exibir o stream/preview em proporção 16:9. *(Frontend: `CamerasView.vue`)*

### 6.6 Leitoras
- **FR-16** — O sistema deve exibir tabela de antenas com dispositivo, IP, status e última leitura. *(Frontend: `LeiturasView.vue` — dados mockados)*
- **FR-17** — O analista deve poder acionar o comando de **reinício** por antena. *(Frontend: `LeiturasView.vue` — simulado com `alert`)*

### 6.7 API geral
- **FR-18** — A API deve expor um endpoint de healthcheck (`GET /health`) indicando status e conectividade com o banco. *(Backend: `GET /health`)*
- **FR-19** — A API deve permitir CORS de qualquer origem (modo dev). *(Backend: `CORSMiddleware`)*

## 7. Requisitos Não-Funcionais

| Categoria | Requisito | Detalhe |
|---|---|---|
| **Performance** | Atualização em tempo real | Dashboard refresca a cada ≤ 5s sem degradação perceptível |
| **Performance** | Leitura de banco | Consultas agregadas (`/stats`) devem retornar em < 500ms |
| **Segurança** | Acesso ao banco | Banco SQLite deve ser lido como **read-only** pela API (sem escrita acidental) |
| **Segurança** | CORS | Em produção, restringir origens permitidas (hoje `*` apenas para dev) |
| **Disponibilidade** | Healthcheck | Endpoint `/health` deve refletir disponibilidade da API e do banco |
| **Portabilidade** | Conteinerização | API e frontend devem rodar via Docker Compose em ambiente isolado |
| **Compatibilidade** | Frontend | Suportar navegadores modernos (Chrome/Edge/Firefox); Node ≥ 20 |
| **Observabilidade** | Logs | API deve logar erros de agregação sem interromper o serviço |
| **Manutenibilidade** | Organização | Rotas da API e views do frontend separadas por módulo |

## 8. Roadmap

### V1 — Base (em andamento)
- [x] API FastAPI com stats, monitoramento e transações
- [x] Dashboard Vue com polling de 5s
- [x] Validação de arquivos + badge de erros
- [x] Páginas de Câmeras e Leitoras (UI)
- [x] Simulador de banco + Docker Compose
- [ ] Integração dos dados reais de validação de arquivos via API
- [ ] Configuração dinâmica dos dispositivos monitorados

### V2 — Operacional (próximo)
- **Diagnóstico de VPAR:** verificação automatizada de status de licença e funcionamento do software de reconhecimento de placas.
- **Saúde do sistema:** alertas sobre equipamentos travados ou falhas de comunicação recorrentes (agregação por janela de tempo).
- **Câmeras reais:** exibição de streams reais (RTSP) com status de conectividade.
- **Leitoras reais:** comando de reinício efetivo via API + histórico de última leitura.
- **Autenticação e roles:** login com perfis (analista, supervisor, admin).
- **WebSockets:** substituir o polling por atualização push em tempo real.

### V3 — Analítica & Proativa
- **Histórico persistente:** séries temporais de status para análise de recorrência de falhas.
- **Alertas ativos:** notificações por e-mail/WhatsApp com base em regras de threshold.
- **KPIs de operação:** MTTR, tempo de pista parada, recorrência por equipamento.
- **Integração com Zabbix:** consumir métricas do `zabbix_agent2` para enriquecer o monitoramento.
- **Multi-posto:** agregação de vários postos em um único painel.
- **Testes automatizados:** cobertura de API (pytest) e frontend (component tests).

## 9. Anexo — Arquitetura Atual

### 9.1 Diagrama de serviços

```
┌─────────────────────┐   HTTP (polling 5s)   ┌──────────────────────┐
│  Frontend (Vue 3)   │ ─────────────────────► │   API (FastAPI)      │
│  Vite / Tailwind    │                        │  GET /stats          │
│  porta 5173         │ ◄───────────────────── │  GET /monitoramento  │
│                     │        JSON            │  GET /transacoes     │
│  Sidebar + Router   │                        │  GET /health         │
└─────────────────────┘                        └──────────┬───────────┘
                                                          │ sqlite3 (read)
                                                   ┌──────▼───────────┐
                                                   │ SQLite           │
                                                   │ abastece.db      │
                                                   │ (data/)          │
                                                   └──────────────────┘
```

### 9.2 Fluxo de dados
1. `scripts/simulador_posto.py` cria o banco `data/abastece.db` com a tabela `transacoes` (pista, veiculo_tag, valor, status).
2. A API lê o banco (path `/var/abastece/dados/abastece.db`, montado via volume no Docker) e agrega as métricas.
3. O frontend consulta a API a cada 5s e renderiza stats, cards de dispositivos e últimas transações.

### 9.3 Componentes mapeados
| Camada | Artefatos |
|---|---|
| Backend | `backend/app/main.py`, `backend/requirements.txt`, `backend/Dockerfile` |
| Frontend | `frontend/src/views/*`, `frontend/src/components/*`, `frontend/src/store.js`, `frontend/src/router/index.js` |
| Infra | `docker-compose.yml`, `backend/Dockerfile`, `frontend/Dockerfile` |
| Dados | `data/abastece.db`, `scripts/simulador_posto.py` |

---

## 10. Critérios de Aceite (V1)

- [ ] Dashboard exibe online/offline de todos os equipamentos cadastrados.
- [ ] Vendas do dia e contagem de sucesso/falhas aparecem corretamente.
- [ ] Últimas 5 transações aparecem com horário, placa, valor e status colorido.
- [ ] Badge de erros na sidebar reflete os arquivos com status `ERRO`.
- [ ] Páginas de Câmeras e Leitoras renderizam com dados (reais ou mock).
- [ ] Toda a solução sobe com `docker compose up` e a API responde em `http://localhost:8000`.

---

*Documento vivo — atualizar a cada iteração conforme novas features entram no backlog.*
