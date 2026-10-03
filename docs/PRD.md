# PRD — Analista SemParar

**Product Requirements Document**

| Campo | Detalhe |
|---|---|
| **Produto** | Analista SemParar |
| **Versão do documento** | 1.3 |
| **Status** | **V1 destravada no código** — #63 (API key opt-in) e #64 (preflight CORS) entregues; falta a confirmação no browser (#67) |
| **Data** | 03/10/2026 |
| **Última revisão** | 03/10/2026 — [#64](https://github.com/OsirisMariano/analsita/issues/64) (preflight CORS) |
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
| Página de Câmeras | Grid de visualização de streams VPAR/CFTV | ⚠️ **Moldura, não produto** — UI pronta, dados mockados (`CamerasView.vue`). Valor real só na V2 (RTSP) |
| Página de Leitoras | Status das antenas + ação de reinício | ⚠️ **Moldura, não produto** — UI pronta, reinício **simulado** via `alert`. Valor real só na V2 |
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
- **FR-11** — O sistema deve listar os arquivos de configuração críticos do posto (ex.: `posto.json`, `concentrador.json`, `sensor.json`, `ifadapter.ini`, licença VPAR, certificado P12, `zabbix_agent2.conf`, `config.json`). *(Backend: `ARQUIVOS_CONFIG` em `backend/app/arquivos_config.py` — 15 entradas; exposto via `GET /arquivos`; consumido em `frontend/src/store.js`)*
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
- **FR-19** — A API deve **restringir as origens CORS a uma allowlist** configurável por ambiente, e **exigir o header `X-API-Key`** em todas as rotas de dados **quando `API_KEY` estiver definida no ambiente**. Rotas isentas de autenticação: `/health`, `/docs`, `/openapi.json`, `/redoc`. O preflight (`OPTIONS`) é **isento por método** em qualquer rota, para que o `CORSMiddleware` possa respondê-lo. *(Backend: `CORSMiddleware` com `CORS_ORIGINS`; `ApiKeyMiddleware` com `Rotas_Isentas` e `Metodos_Isentos`)*

> **Histórico desta alteração (02/10/2026, [#68](https://github.com/OsirisMariano/analsita/issues/68))**
> A redação anterior dizia *"CORS de qualquer origem (modo dev)"*. Isso foi **obsoleto na prática**: a sprint de segurança (SEC-01 a SEC-05, PR #59) trocou `*` por allowlist via `CORS_ORIGINS` **e** passou a exigir `X-API-Key`. O requisito agora documenta o comportamento **real** do código (`backend/app/main.py:22-88`).
>
> **Consequência resolvida em 03/10/2026 ([#63](https://github.com/OsirisMariano/analsita/issues/63) + [#64](https://github.com/OsirisMariano/analsita/issues/64)).**
> Restavam duas causas combinadas: o frontend **não envia `X-API-Key`** (0 ocorrências em `frontend/src`) e o middleware **não isentava `OPTIONS`**, então o preflight morria com 403 e o painel não carregava.
> - **#63** — `API_KEY` passou a ser **opt-in**: ausente, o middleware não exige credencial. O frontend sem header deixou de ser um problema.
> - **#64** — `OPTIONS` passou a ser **isento por método** (`Metodos_Isentos`), então o preflight é respondido pelo `CORSMiddleware`. O `GET` continua exigindo a chave normalmente quando `API_KEY` está definida.
>
> ⚠️ **O frontend segue sem enviar `X-API-Key`** — e isso está correto na V1: a autenticação é opt-in e o ambiente de estudo não exige credencial.
>
> > **Por que #64 era necessária mesmo sem o header no frontend hoje:** header customizado **obriga** preflight. Sem a isenção, o momento em que alguém adicionasse `X-API-Key` ao `fetch` — o passo natural ao plugar a #53 no futuro — o painel quebraria de novo, desta vez com um erro genérico no console em vez de um 403 legível. A armadilha foi desarmada antes de alguém cair nela.

## 7. Requisitos Não-Funcionais

| Categoria | Requisito | Detalhe |
|---|---|---|
| **Performance** | Atualização em tempo real | Dashboard refresca a cada ≤ 5s sem degradação perceptível |
| **Performance** | Leitura de banco | Consultas agregadas (`/stats`) devem retornar em < 500ms |
| **Segurança** | Acesso ao banco | ⚠️ **Não garantido pela infra.** A API só faz `SELECT`, mas `docker-compose.yml:18` monta `./data:/var/abastece/dados` **sem `:ro`**. O requisito real é "a API não escreve"; o isolamento de filesystem **não** está implementado. Corrigir com #67 |
| **Segurança** | CORS | ✅ **Já restrito** via allowlist `CORS_ORIGINS` (SEC-01). Não existe mais `*` em nenhum ambiente |
| **Disponibilidade** | Healthcheck | Endpoint `/health` deve refletir disponibilidade da API e do banco |
| **Portabilidade** | Conteinerização | API e frontend devem rodar via Docker Compose em ambiente isolado |
| **Compatibilidade** | Frontend | Suportar navegadores modernos (Chrome/Edge/Firefox); Node ≥ 20 |
| **Observabilidade** | Logs | API deve logar erros de agregação sem interromper o serviço |
| **Manutenibilidade** | Organização | Rotas da API e views do frontend separadas por módulo |

## 8. Roadmap

### V1 — Base (entregue em código; confirmação no browser pendente)
- [x] API FastAPI com stats, monitoramento e transações
- [x] Dashboard Vue com polling de 5s
- [x] Validação de arquivos + badge de erros
- [x] Páginas de Câmeras e Leitoras (UI — moldura, dados mockados)
- [x] Simulador de banco + Docker Compose
- [x] Integração dos dados reais de validação de arquivos via API — ✅ **JÁ IMPLEMENTADA** (`GET /arquivos` e `GET /validacao-dados` retornam dados reais do backend). Estava marcada como pendente por engano. *Não* é mais item de backlog: o destravamento do 403 foi feito em #63 + #64
- [ ] ~~Configuração dinâmica dos dispositivos monitorados~~ — 🔀 **DECISÃO DO PO (02/10): movida para a V2.** Na V1, a configuração se faz por variável de ambiente `EQUIPAMENTOS` (JSON), já implementada em `backend/app/main.py:72-84`. Uma API de configuração dinâmica continua **fora do escopo da V1** (§5.2) e passa a ser item de V2

> **Por que a V1 está "entregue em código" mas não funciona:** o painel não carrega por um defeito de autenticação, não por falta de funcionalidade. Ver §11.

### V2 — Operacional (próximo)
- **Diagnóstico de VPAR:** verificação automatizada de status de licença e funcionamento do software de reconhecimento de placas.
- **Saúde do sistema:** alertas sobre equipamentos travados ou falhas de comunicação recorrentes (agregação por janela de tempo).
- **Câmeras reais:** exibição de streams reais (RTSP) com status de conectividade.
- **Leitoras reais:** comando de reinício efetivo via API + histórico de última leitura.
- **Autenticação e roles:** login com perfis (analista, supervisor, admin).
- **Configuração dinâmica dos dispositivos:** API para listar/editar os equipamentos monitorados, hoje fixos em `_DEFAULT_EQUIPAMENTOS` (promovido da V1 em 02/10).
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

> **Estado em 03/10/2026:** o bloqueio de runtime foi removido — #63 (API key opt-in) e #64 (preflight CORS) estão entregues. O que falta é a **verificação no browser**, que é o rito da #67.
> Regra de marcação (inalterada): só marcar `[x]` com evidência observada no browser, nunca por leitura de código. Por isso os itens abaixo continuam **[ ]** — implements e testado, porém não observado no browser ainda.
> Exceção: o critério de `OPTIONS` foi marcado por ter evidência de runtime direta (pytest + `curl` contra servidor real), detalhada na linha correspondente.

- [ ] ⏳ Dashboard exibe online/offline de todos os equipamentos cadastrados. — *implementado (`/stats`); aguardando confirmação no browser (#67)*
- [ ] ⏳ Vendas do dia e contagem de sucesso/falhas aparecem corretamente. — *implementado (`/stats`); aguardando confirmação no browser (#67)*
- [ ] ⏳ Últimas 5 transações aparecem com horário, placa, valor e status colorido. — *implementado (`LIMIT 5` + CSS de cores); aguardando confirmação no browser (#67)*
- [ ] ⏳ Badge de erros na sidebar reflete os arquivos com status `ERRO`. — *implementado (`store.totalErros`); aguardando confirmação no browser (#67)*
- [ ] ⏳ Páginas de Câmeras e Leitoras renderizam com dados (reais ou mock). — *implementado; aguardando confirmação no browser (#67)*
- [ ] ⏳ Toda a solução sobe com `docker compose up` e a API responde em `http://localhost:8000`. — *build validado na CI; validação integrada é a #67*
- [x] `OPTIONS` em rota pública não retorna 403. — ✅ **Corrigido em #64.** Evidência de runtime, **não** de browser: pytest parametrizado nas 7 rotas públicas (falha em 16 casos ao remover a isenção) + `curl` contra `uvicorn` real devolvendo `200` com `access-control-allow-origin`; origem não permitida segue sem o cabeçalho (SEC-01) e `GET` sem chave segue em `403`. Confirmação no browser fica para a #67.

---

## 11. Reclassificação do Projeto & Estado Real (decisão de 01–02/10/2026)

> Registrado aqui para que a confusão entre docs e código não se repita. Fonte: [#62](https://github.com/OsirisMariano/analsita/issues/62), [#68](https://github.com/OsirisMariano/analsita/issues/68).

### 11.1 Natureza do projeto
O Analista SemParar é **projeto de estudos**, não produto em produção. Não há cliente, SLA, ambiente produtivo nem operação contínua. Isso **remove a segurança do caminho crítico**: endurecimento não pode consumir a entrega da funcionalidade.

### 11.2 Decisões do PO (01/10/2026)

| Tema | Decisão | Consequência |
|---|---|---|
| Autenticação | **Fora da V1.** `API_KEY` fica no código, mas vira **opt-in** | Issue #63 |
| CORS | **Mantém restrito** a `localhost:5173` | Custa zero, evita ruído de erro |
| Épico 6 (build de produção) | **Cancelado** | `serve` não agrega valor de estudo sem auth real |
| #52 (TLS), #53 (login), #54 (rate limit), #55 (logging estruturado) | **Backlog sem prazo** | Reescritos quando as funções estiverem definidas |
| FR-03 (polling 5s) | **Corrige** | Issue #65 |

### 11.3 Custo da sprint de segurança
A sprint consumiu **42 SP** e entregou 5 de 6 épicos. Nesse intervalo **a V1 funcional nunca foi demonstrada funcionando**. É o registro de que hardening sem verificação end-to-end produz entregas que não rodam.
### 11.4 Bloqueio da V1 e como foi removido

**Estado em 02/10/2026:** toda chamada do frontend à API retornava **403**, por duas causas somadas:

1. O frontend **não envia `X-API-Key`** — 0 ocorrências em `frontend/src`. Correção: **#63** (API key opt-in).
2. O `ApiKeyMiddleware` **não isentava `OPTIONS`**. Ele é a camada mais externa (adicionado depois do `CORSMiddleware`, porque `add_middleware` insere no início da pilha), então interceptava e rejeitava o preflight antes de o CORS responder. Correção: **#64** (`Metodos_Isentos = {"OPTIONS"}`).

**Estado em 03/10/2026:** ambas entregues. `GET /stats`, `/monitoramento`, `/transacoes`, `/arquivos` e `/validacao-dados` respondem **200** no fluxo normal e o preflight responde **200** nas 7 rotas. Falta apenas a confirmação no browser, que é o rito da **#67**.

> ⚠️ **Sobre a numeração de linhas:** o `ApiKeyMiddleware` ocupa `backend/app/main.py:54-88` na revisão de 03/10. A referência `41-48` aqui estava defasada desde a #63.

> **Por que a CI não pegou o preflight — com uma correção ao diagnóstico original.** A versão anterior deste documento afirmava que o `TestClient` *"não simula preflight CORS"*. **Isso estava errado**, verificado em 03/10: o `TestClient` **executa** o caminho de `OPTIONS` de verdade quando o teste o solicita explicitamente — a requisição percorre a pilha de middlewares e o `CORSMiddleware` responde com os cabeçalhos corretos.
>
> A lacuna real era mais estreita: existia um teste de preflight, mas **só para o caso `API_KEY` ausente** — exatamente o caso que **não** quebrava, porque sem chave o middleware fica inativo. O cenário com `API_KEY` ativa, que é o que devolvia 403, **não tinha cobertura nenhuma**. O `TestClient` não era o problema; a ausência de parametrização sobre as rotas e sobre os dois estados da chave era.
>
> Isso é a mesma lição da §11.3 com um sabor diferente: a cobertura existia, mas cobria o caminho que **já** funcionava.

### 11.5 Regra permanente
> **Toda task que altera comportamento observável atualiza este PRD no mesmo PR.**

Já valia desde a v1.0 (ver rodapé, *"Documento vivo"*) e não foi cumprido — a divergência do FR-19 custou a §11 inteira. A auditoria FR-01..FR-19 de 02/10 fica registrada abaixo.

### 11.6 Auditoria FR-01..FR-19 contra o código (02/10/2026)

| FR | Veredito | Evidência |
|---|---|---|
| FR-01 | ✅ Conforme no código | `GET /stats` → `monitoramento`. Destravado em runtime por §11.4 |
| FR-02 | ✅ Conforme | `GET /stats` → `transacoes` |
| FR-03 | ⚠️ **Parcial** | `setInterval(carregarDados, 5000)` existe (`HomeView.vue:34`), mas `carregarDados` é `async` **sem guarda de sobreposição** — requisições lentas acumulam. Issue #65 |
| FR-04 | ✅ Conforme | `disparar_ping()`: `ping -c 1 -W 1` + gate `ip_address()` (SEC-06) |
| FR-05 | ✅ Conforme | `_DEFAULT_EQUIPAMENTOS` (`main.py:118-124`) |
| FR-06 | ✅ Conforme | `DispositivoCard.vue` |
| FR-07 | ✅ Conforme | `GET /monitoramento` → nome, ip, status |
| FR-08 | ✅ Conforme | `ORDER BY timestamp DESC` (`main.py:248`) |
| FR-09 | ✅ Conforme | `LIMIT 5` em `lista_detalhada` (`main.py:248`) |
| FR-10 | ✅ Conforme | CSS `.concluido` / `.em-aberto` / `.falha` (`TabelaTransacoes.vue:94-107`) |
| FR-11 | 🔧 **Corrigido nesta revisão** | Mapeamento estava errado: a lista vive em `backend/app/arquivos_config.py` (15 entradas), não em `store.js`, que apenas consome `GET /arquivos` |
| FR-12 | ✅ Conforme | `ValidacaoArquivosView.vue:34-38` |
| FR-13 | ✅ Conforme | `AppSidebar.vue:100-108` + `store.js:32` (`totalErros`) |
| FR-14 | ⚠️ Conforme, mas **mockado** | `CamerasView.vue:3-5` — 3 câmeras com placeholder |
| FR-15 | ✅ Conforme | `aspect-video` = 16:9 (`CamerasView.vue:27`) |
| FR-16 | ⚠️ Conforme, mas **mockado** | `LeiturasView.vue` |
| FR-17 | ✅ Conforme (simulado) | `alert()` — coerente com §5.2 |
| FR-18 | ✅ Conforme | `GET /health` |
| FR-19 | 🔧 **Corrigido em 02/10, refined em 03/10** | Allowlist `CORS_ORIGINS` + `X-API-Key` obrigatório **quando `API_KEY` está definida** (opt-in, #63) + `OPTIONS` isento por método (#64). Ver §6.7 |

**Resumo da auditoria:** 14 conformes, 1 corrigido (FR-19), 1 corrigido (FR-11), 2 mockados por decisão de escopo (FR-14/16), 1 parcial com issue aberta (FR-03).
**Nenhum requisito da §6 está ausente no código.** O bloqueio era de integração (§11.4) e foi removido em 03/10; falta a confirmação no browser (#67).

---

*Documento vivo — atualizar a cada iteração conforme novas features entram no backlog.*
*Regra: toda alteração de comportamento observável atualiza este documento no mesmo PR (§11.5).*
