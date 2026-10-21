# Diário de Bordo — Sprint V1 Funcional: Segurança

> Arquivo rolante para retomada rápida do trabalho. Dia mais recente no topo.
> Board: https://github.com/users/OsirisMariano/projects/70

---

## 🗓️ Quarta, 21/10 (noite, parte 6) — Reescopo do É8 por capacidade: 40 SP, 4 ciclos, 2 milestones novos

> A parte 5 planejou o É8 com 59 SP em 3 ondas. Esta entrada registra a resposta de capacidade que veio depois — **2 h/dia** — e o reescopo que ela obriga. O plano da parte 5 vira histórico; o plano vivo está em [`docs/sprint-e8-seguranca-evolucao.md`](sprint-e8-seguranca-evolucao.md) e na §12 do PRD.

### A pergunta que não tinha sido feita

A parte 5 respondeu *"o que fazer"*. Não respondeu *"com que frequência"*. A pergunta apareceu quando o dono do projeto respondeu três coisas: **é um portfólio, não tem cliente, e são 2 h por dia** — com a nota de que a **C1** (transferir a #52 para a V2) já estava confirmada.

A resposta a "2 h/dia" expôs um erro do plano: a **capacidade** nunca foi medida, foi herdada.

### O erro: "42 SP em 6 dias (≈ 7 SP/dia)" era previsão, não fato

O plano da parte 5 se apoiou nessa frase, que está no doc da sprint anterior como **"duração *estimada*: 6 dias úteis"**. O que o histórico mostra:

| | |
|---|---|
| Período real | 24/08 (seg) → 10/09 (qui) = **14 dias úteis de calendário** |
| Entradas no diário | 24/08, 25/08, **05/09 (sábado)**, 09/09, 10/09 — com um **buraco de 9 dias corridos** (26/08 → 04/09) |
| Entregue | **36 dos 42 SP** (o É6 foi cancelado) |
| **Unidade real de ritmo** | **SP por sessão de trabalho** — não SP por dia de calendário |

Ou seja: 36 SP em **~5 sessões concentradas** espalhadas por 3 semanas. A "referência de 7 SP/dia" era a previsão de uma sessão de **dia inteiro**. A 2 h/dia, a métrica honesta é **SP por sessão**.

### A correção do invariante: o número que "virou verdade" expira

Vale registrar porque quase passou: o AC de **R$ 803,85 / 5 / 3** está no PRD, no doc do É8 e na issue #51. Ele é **verdade para o banco semeado hoje**. O `/stats` filtra `date(timestamp) = date('now','localtime')` (correção do #81) e as transações "de hoje" são carimbadas **no momento da simulação** — um banco gerado ontem devolve **R$ 0,00** hoje, sem que nada de código tenha mudado.

Sem isso registrado, o próximo rito falha por um motivo que não tem relação com o código em revisão — e a reação natural da equipe é *"o AC está desatualizado"*.

> **A invariante virou procedimento:**
> ```bash
> SIMULADOR_SEED=154622 python scripts/simulador_posto.py
> ```
> *"as transações de hoje do banco semeado: 5 `CONCLUIDO` somando **R$ 803,85**, 2 `EM_ABERTO`, 3 `FALHA`"*.
> O **valor** é fixo pela semente; a **data** é a de hoje. Registrado em 3 lugares: PRD §12.3, doc do É8 §10 e AC da #51.

### O reescopo: 59 SP → 40 SP, 3 ondas → 4 ciclos

| | Antes (parte 5) | Agora |
|---|---|---|
| Escopo | 59 SP, 5 issues | **40 SP, 3 issues** (#51, #53, #55) |
| #52 (TLS, 10 SP) | É8, Onda 3 condicionada | → **milestone "V2 — Operacional"** (D3) |
| #54 (rate limit, 11 SP) | É8, Onda 2 | → **milestone "É9 — Hardening follow-up"** (D7) |
| Janela | 26/10 → 06/11 | 26/10 → **04/12**, checkpoint **13/11** |
| Trilha de auditoria | 3 SP (log) | **5 SP** — com a **É8-27b** (2 SP): `GET /auditoria` + card no painel |
| Critério de demo | não existia | **5 itens registrados** (§9 do doc do É8) |

**As 3 decisões novas (D6–D8):**

- **D6 — capacidade = 2 h/dia → ~1,5 SP/sessão.** Três cenários: 2,5 SP/sessão → ~18/11 · **1,5 → ~04/12** · 0,7 → ~15/01. **O ciclo 1 é a medição**; o checkpoint de 13/11 recalibra.
- **D7 — a #54 sai do É8.** 11 SP (20% do orçamento) para o item de menor valor visível do lote. Um portfólio ganha 10x mais com *"a validação saiu assinada"* do que com *"a API devolve 429"*.
- **D8 — a trilha de auditoria vira visível (+2 SP).** Sem card na tela, a história do field service fica no log do servidor — invisível para quem abre o repo. Com ele, a demo conta o fluxo inteiro: técnico entra → painel valida → registro assinado.

**E o que a C1 destravou:** a #52 saiu de "Onda 3 condicionada" para um milestone próprio, com data própria. A parte 5 tinha um dilema sem saída — *"tirá-la do milestone a transformaria em issue órfã"* — que na verdade era o milestone **do É8** segurando issue que não é do É8. A solução não era segurar: era criar o milestone certo.

> **Nenhuma issue fica órfã.** A #52 e a #54 ganharam milestones próprios, e a regra "milestone fecha quando o épico fecha" continua valendo para os três.

### Os 4 ciclos (na ordem da demo)

| Ciclo | Épico | SP | Janela | Artefato |
|---|---|---|---|---|
| 1 | #51 | 6 | 26/10 → 29/10 | "o repo não guarda segredo" + **a taxa medida** |
| 2 | #53 | 20 | 30/10 → 17/11 | **tela de login** |
| 3 | #55a (É8-25, 26, 29, 30) | 7 | 18/11 → 24/11 | log JSON + `request-id` |
| 4 | #55b (É8-27, 28) + **É8-27b** | 7 | 25/11 → 04/12 | 🎯 **a trilha no painel** |

**E a dependência que se desamarrou:** na versão anterior, o épico de logging inteiro dependia da #53. O grafo justificava só **3 dos 12 SP** — a É8-27 (auditoria) precisa saber *quem* acessou, mas log JSON, `request-id` e redaction não dependem de ninguém. 9 SP de logging foram liberados para o ciclo 3 rodar em paralelo.

### O enquadramento honesto: o É8 não dá agilidade

O dono do projeto deu a nota de ordem do produto: **"um sistema como esse pode ser útil para o field service que está no posto de combustível e precisa de agilidade na hora de validar os equipamentos"**.

O É8 **não dá agilidade**. Agilidade real — reinício de leitora, diagnóstico de VPAR, câmeras reais — é a **V2** (FR-14/16/17). O É8 dá **rastreabilidade**: *quem* validou, *quando*, *com que resultado*. A distinção está no doc do É8 §1 e no PRD §12.5, porque um portfólio que promete agilidade e entrega login erra o Expectations no teste — e a demo (§9) existe justamente para não errar.

### O que foi feito nesta noite

- **Doc do É8 reescrito** — 4 ciclos, taxa real, D1–D8, É8-27b, §9 (critério de demo), §3.1 (relatório da auditoria É8-01), 12 passos de rito
- **PRD §12 reescrito** — D1–D8, 40 SP, 4 ciclos, a correção do invariante (§12.3) e a §12.5 reescrita
- **`docs/sprint-v1-funcional-seguranca.md`** — tabela de rastreabilidade atualizada (#52 → V2, #54 → É9)
- **Milestones novos** — "V2 — Operacional" (#52) e "É9 — Hardening follow-up" (#54); milestone É8 reescrito com 40 SP e `due_on` 04/12/2026
- **5 issues reescritas** com os ciclos, o É8-27b e os ACs corrigidos; #52 e #54 com comentário de transferência
- **É8-01 concluída** — auditoria dos 19 arquivos: **0 segredo real**, **3 IPs de LAN em 7 mocks**, 8 arquivos sensíveis por definição; histórico do git **não** precisa ser reescrito (a providência, se um dia entrar um segredo, é **rotacionar**)

---

## 🗓️ Quarta, 21/10 (noite, parte 5) — Planejamento do É8: 5 decisões, 59 SP, 3 ondas

> ⚠️ **Esta entrada é histórico.** O plano foi reescopado na **parte 6** (mesma noite): 59 SP → **40 SP**, 3 ondas → **4 ciclos**, #52 e #54 transferidas para milestones próprios, `due_on` 06/11 → **04/12**. As decisões D3 e D5 abaixo foram **substituídas** por D3/D7 (transferência) e D5/D6 (capacidade). O plano vivo está em [`docs/sprint-e8-seguranca-evolucao.md`](sprint-e8-seguranca-evolucao.md).

> A entrada anterior fechou o container. Esta abre o conteúdo: o É8 deixou de ser "5 pendências de segurança sem prazo" e virou um sprint com função definida, tasks com critério de aceite, story points e data.

### O que a §11.2 exigia e o que faltava

O PRD §11.2 classificava #52, #53, #54 e #55 como *"backlog sem prazo — reescritos quando as funções estiverem definidas"*. A #51 entrava na mesma lista pelo título. **Função definida** era o que faltava: as 5 issues diziam *o quê* fazer ("evoluir para autenticação completa", "aplicar rate limiting") e não diziam **quem faz o quê, até onde, e como se sabe que acabou**.

Planejar exige decidir o que as issues não decidiam. São 5 decisões, e elas não são técnicas — são de escopo.

### As 5 decisões

| # | Decisão | Escolha |
|---|---|---|
| **D1** | Onde fica a identidade? | **`auth.db` separado** (SQLite gravável) |
| **D2** | Onde fica o rate limit? | **In-process** (FastAPI), chave por IP/cliente |
| **D3** | A #52 (TLS) executa no É8? | Escopo sim, **Onda 3 (condicionada)**; recomendação do PO: transferir para a V2 |
| **D4** | Roles entram? | **Não** — identidade + 1 nível (`admin`/leitura). A matriz é item da V2 |
| **D5** | Quando fecha? | **06/11/2026**, começando em 26/10/2026 |

**D1 e D2 vieram do código, não da preferência do PO.** A API abre o banco de transactions com `mode=ro` (§7) — ela **não pode** gravar uma tabela de usuários no mesmo arquivo. Daí o `auth.db` separado; e como o limite é in-process, a #54 **não** depende da #52, e as ondas rodam em paralelo.

**D3 é a decisão que este planejamento custou mais.** A #52 é o épico de **menor valor e maior risco** do lote: certificado self-signed, sem cliente, sem domínio e sem operação contínua (§11.1) protege uma rede que não existe — e é o que mais pode quebrar a V1, porque muda a origem do CORS, a URL da API e o preflight. A recomendação é **transferi-la para a V2**, onde já existem frontend de produção e operação real. Mas a #52 **fica** no milestone: tirá-la de lá a transformaria em issue órfã, que é exatamente o problema que a parte 4 desta noite acabou de resolver. Fica na **Onda 3**, a última, e a decisão de executar ou transferir se toma no fim da Onda 2.

### A auditoria que mudou o escopo antes de estimar

Antes de dar número, o PO auditou o código. **Três achados reescreveram o plano:**

1. **Não existe segredo no `mock_data/` hoje.** Os 19 arquivos versionados são placeholders: `licenca.V2C` = "mock license data", `cert.p12` = "mock certificate", `zabbix_agent2.conf` = `Server=192.0.2.1` (RFC 5737). O único dado não-placeholder são **3 IPs de LAN** em 7 arquivos de mock. A #51 deixou de ser "limpeza" e virou **guardrail de futuro** — e, por não haver segredo real, **o histórico do git não precisa ser reescrito**. Reescrever invalidaria as tags `v1.0.0`/`v1.0.1` sem comprar segurança nenhuma.
2. **A API é `mode=ro`.** Uma tabela de usuários no mesmo banco é impossível (D1).
3. **O frontend não tem nenhuma ocorrência de `login`/`token`/`Authorization`** (0 hits em `frontend/src/`). Autenticação obrigatória sem tela de login quebraria o painel — exatamente o 403 da §11.4. Daí o **modo opt-in** (`AUTH_ENABLED`), que espelha o padrão que a #63 já provou para a API Key.

> **O terceiro achado é a armadilha do É8 inteira.** Se alguém implementar a #53 sem a tela de login e sem o modo opt-in, o produto fica igual estava em 03/10 — a tela não abre — e o É8 vira mais uma entrega de hardening que ninguém viu. Por isso o rito de 8 passos entra **por épico**, e o AC da #53 exige o rito **nos dois modos** (ligado e desligado).

### O plano

**59 SP em 3 ondas** (a sprint anterior entregou 42 SP em 6 dias, ≈7 SP/dia):

| Onda | Épicos | SP | Janela |
|---|---|---|---|
| 1 | #51 (6) + #53 (20) | 26 | 26/10 → 29/10 |
| 2 | #55 (12) + #54 (11) | 23 | 30/10 → 04/11 |
| 3 | #52 (10) — **condicionada** | 10 | 05/11 → 06/11 |

**A #53 vem primeiro porque é a peça central:** a auditoria da #55 precisa saber **quem** acessou, e a #54 fica melhor com chave por usuário do que só por IP. A #51 é a mais independente do lote — guardrail barato, fecha rápido, não bloqueia nada.

**O número que decide o rate limit:** o dashboard faz polling a cada 5 s = **12 req/min** por cliente. Limite abaixo de ~30/min **derruba o produto** — por isso há AC explícito de que o polling normal nunca toma 429.

### O que foi materializado

- `docs/sprint-e8-seguranca-evolucao.md` — o doc do sprint: decisões, 5 épicos com tasks/SP/AC, ondas, dependências, DoR (**nova**), DoD, rito de 12 passos, KPIs, riscos, fora de escopo.
- **As 5 issues reescritas** (#51–#55): função definida, tabela de tasks com AC, critérios de aceite em BDD, dependências e "fora do escopo" — e o label `backlog-futuro` trocado por `sprint-e8`.
- **PRD v1.7**: nova **§12** (resumo executivo do É8), §5.2 e §8 V2 com referência cruzada, §11.2 marcada como cumprida.
- `docs/sprint-v1-funcional-seguranca.md`: a lista "Pendências futuras" virou **tabela de rastreabilidade** L-1/L-2 → issue → onde está agora.
- Milestone É8 com **descrição do plano** e prazo **06/11/2026** no campo `due_on` (a data que ficou sem prazo na parte 4). O **início em 26/10** está no texto da descrição e nos docs — a API do GitHub só aceita `start_on` na criação do milestone, e este foi criado antes do planejamento.
- Board: #51–#55 movidas de `📋 BACKLOG` para `📥 TO DO`.

### Estado final

| | |
|---|---|
| Milestone É8 | `open`, 26/10 → 06/11/2026, 5 issues |
| Issues | 5 reescritas, 59 SP no total, 0 soltas |
| Board | 5 em `📥 TO DO` |
| Execução | **nenhuma task iniciada** — este registro é só o plano |

> **A lição continua sendo a mesma das outras três desta semana, e ela é sobre método.** A parte 4 mostrou que faltava uma regra para fechar container. Esta mostra que faltava **decisão** para abrir sprint. As duas coisas são o mesmo defeito: o projeto tinha 5 pendências de segurança com o formato de desabafo ("aplicar rate limiting", "evoluir para autenticação completa") e nenhum formato de decisão. **Pendência sem decisão é dívida; dívida com data é plano.**

---


> O `main` estava correto, o código estava correto, os 54 issues estavam fechados — e mesmo assim a aba de milestones do repositório mostrava **7 épicos em andamento, todos atrasados**. Nenhum trabalho estava em andamento. Era só um container que ninguém fechava.

## 🗓️ Quarta, 21/10 (noite, parte 4) — Higiene do GitHub: os 7 milestones do É1..É7 fechados, É8 criado

> O `main` estava correto, o código estava correto, os 54 issues estavam fechados — e mesmo assim a aba de milestones do repositório mostrava **7 épicos em andamento, todos atrasados**. Nenhum trabalho estava em andamento. Era só um container que ninguém fechava.

### O que estava errado

| Milestone | Estado | Issues abertas | Prazo |
|---|---|---|---|
| #1 É3 — Docker Hardening | `open` | 0 | 25/08 |
| #2 É2 — Input Validation | `open` | 0 | 25/08 |
| #3 É1 — CORS + Autenticação | `open` | 0 | 27/08 |
| #4 É5 — Configuração + Segredos | `open` | 0 | 27/08 |
| #5 É4 — Error Handling | `open` | 0 | 28/08 |
| #6 É6 — Frontend Produção | `open` | 0 | 31/08 |
| #7 É7 — V1 Funcional | `open` | 0 | 15/10 |

Sete milestones abertos, **zero** issues abertas em qualquer milestone do repositório, todos os prazos vencidos (hoje é 21/10). E o trabalho de cada um comprovadamente encerrado, por três vias independentes: os issues de épico fechados (6 como `completed`, o É6 como `not_planned`), a descrição do milestone É7 ("Substitui o É6 (cancelado)") e o PRD §11 ("Épico 6 (build de produção) | **Cancelado**").

### Por que ninguém fechou

O GitHub **nunca fecha milestone sozinho** — é um passo manual, como `gh issue close`. E o projeto tem disciplina nesse ponto: fechou **54 de 54** issues com motivo explícito (47 `completed` + 7 `not_planned`). O milestone era o único container sem dono do passo, porque **nenhum documento dizia que ele também fecha**. Não havia `AGENTS.md`, nem `CONTRIBUTING.md`, nem seção no doc de sprint sobre isso.

Faltava a regra, não o esforço.

### O que custava

A aba de milestones abertos é, por convenção do GitHub, o painel de "o que está em andamento". Ela dizia **"7 em andamento, todos atrasados"** quando o quadro real era **"0 em andamento"**. Sinal invertido é pior que sinal ausente: treina o olho a ignorar o campo, e faz a lista parecer um backlog de 7 épicos abertos no momento de planejar o É8 — o É6, que é o único com uma decisão real por trás (cancelado), ficava indistinguível dos demais.

### O que foi feito

**1. Os 7 milestones fechados** (`PATCH /milestones/{N}` com `state=closed`), todos em 21/10/2026 18:16 UTC.

Fechar milestone **não** mexe nas issues: os `stateReason` foram preservados — o #18 (É6) continua `not_planned` e o #62 (É7) continua `completed`. A distinção "entregue" vs "cancelado" vive na issue, que é onde ela deve viver.

**2. O milestone É8 criado** — "É8 — Segurança & Evolução", com as 5 issues de segurança que estavam **sem milestone nenhum** (#51 L-1, #52 TLS, #53 auth real, #54 rate limit, #55 logging) ligadas a ele e com responsável atribuído. A descrição registra a precedência que o próprio #53 impõe: rate limit, logging e TLS dependem de saber **quem** está autenticado, então #53 vem primeiro.

**Sem prazo, de propósito.** Os 7 milestones antigos tinham data, mas o É8 não foi estimado em story points — diferente da sprint anterior, que tinha 42 SP e 6 dias definidos no doc. Inventar uma data seria repetir o que a §11 do PRD critica: entregar sem verificação. O prazo entra junto com o planejamento.

> **Um segundo desvio encontrado na mesma varredura:** das 54 issues fechadas, só **29** têm responsável — as outras 25 foram fechadas sem `assignee`. Não corrigi retroativamente: responsável em issue já encerrada é ruído, e mexer em 25 issues fechadas para "completar um padrão" não entrega nada. Fica registrado aqui como a outra metade da mesma lacuna: o projeto fecha issue com motivo explícito, mas o **campo de responsável nunca foi uma regra** — exatamente como o milestone. A diferença: o responsável é útil nas issues abertas, e as 5 do É8 já foram criada com ele.

**3. A regra escrita** em `docs/sprint-v1-funcional-seguranca.md`, na seção **"GitHub: milestone fecha quando o épico fecha"**, ao lado das outras regras de processo (branch strategy, via de release fora do ciclo, versionamento por tag). E ancorada na **Definition of Pronto**: o checklist "Para a sprint completa" ganhou a linha *"Milestone da sprint fechado"*.

### Estado final

| | |
|---|---|
| Milestones | 7 `closed` (É1..É7) + 1 `open` (É8, 5 issues abertas) |
| Issues abertas | 5 — todas no É8, **nenhuma solta** |
| Issues fechadas | 54 — **todas** com `stateReason` explícito; 29 com responsável |
| Release | **nenhum** — é metadado de processo, não de produto. Vai para `develop` e chega ao `main` no próximo release, como a nota de publicação do #81 |

> **A lição tem a mesma forma das outras duas desta semana.** A política de branches não existia até precisar de um hotfix fora do ciclo. O versionamento por tag não existia até precisar identificar um release. A regra de milestone não existia até precisar de um milestone fechado. **Toda regra de processo deste repositório nasceu de uma exceção** — e o custo de não ter a regra não aparece no código, aparece no painel.

---

## 🗓️ Quarta, 21/10 (noite, parte 3, b) — Publicado: PR #86 mergeado no `main`, tags v1.0.0 e v1.0.1 criadas

> Registro factual do que foi publicado. Os **detalhes e o porquê** estão na entrada anterior (parte 3).

| | |
|---|---|
| **PR** | [#86](https://github.com/OsirisMariano/analsita/pull/86) — `release: develop -> main (v1.0.1 — correção do #81)` — **MERGED** em 21/10/2026 18:00 UTC |
| **Merge commit** | `b2b8b26` (2 pais: `022edd6` = develop, `932f89a` = main anterior) — **merge commit, não squash** |
| **Conteúdo** | `main` e `develop` ficaram **idênticos** (`git diff` vazio) — 7 arquivos, +462/−16 |
| **Tags** | `v1.0.0` → `932f89a` (É7, retroativa) · `v1.0.1` → `b2b8b26` (este release) |
| **CI** | 3/3 verde no PR de release (backend, frontend, build das imagens) |
| **Verificação** | `main:257` já tem `WHERE date(timestamp) = date('now', 'localtime')`; não resta agregação sem filtro; os 4 commits do #81 legíveis no histórico do `main` |

**O conflito que o release teve (e como foi resolvido).** O merge acusou conflito em 4 arquivos — `scripts/simulador_posto.py`, `backend/tests/test_readonly_db.py`, `docs/PRD.md` e o diário. A causa é conhecida e é a mesma do #84: o release do É7 entrou no `main` como **squash**, então o `main` e o `develop` carregam o **mesmo trabalho por caminhos históricos diferentes**, a partir do mesmo ancestral (`bbc8ed3`). Por isso os dois lados mexiam nos mesmos arquivos.

A resolução foi mechanicalamente segura: comparadas as árvores, o `main` (`932f89a`) e o `develop` (`80fb80f`) são **idênticos** — exceto pelas 10 linhas do diário escritas *depois* do release. Ou seja, o `develop` contém todo o conteúdo do `main` mais a correção do #81. Resolver mantendo a versão do `develop` em todos os arquivos conflictedos produz uma árvore **idêntica à do `develop`**, e o diff resultante contra o `main` é exatamente o conjunto de 7 arquivos deste release. Verificado antes de commitar, e o `git diff main develop` está vazio desde então.

> **Lição para o próximo release.** Este conflito era previsível: ele vem do squash do #84, não do conteúdo. A regra nova no doc de sprint (release sempre com merge commit) existe para não repetir isso — com merge commit, o `main` e o `develop` compartilham o ancestral certo e o merge de release não conflita.

---

## 🗓️ Quarta, 21/10 (noite, parte 3) — Release: a correção do #81 vai para o `main` (v1.0.1)

> O É7 já tinha sido publicado. Esta entrada é o release da **correção** que ficou depois dele — e, junto, a política que faltava para que um release fora do ciclo da sprint deixe de ser uma discussão a cada vez.

### O que entra

Exatamente a correção do #81 — **6 arquivos, +370/−14**:

| Arquivo | O que muda |
|---|---|
| `backend/app/main.py` | A agregação do `/stats` recorta por dia: `WHERE date(timestamp) = date('now', 'localtime')` |
| `backend/tests/test_stats_hoje.py` | Novo (6 testes) — o contrato do filtro |
| `backend/tests/test_readonly_db.py` | Fixture com datas relativas (tira a bomba-relógio) |
| `scripts/simulador_posto.py` | Gera 6 transações de dias anteriores + `str(datetime)` no lugar do adaptador deprecado |
| `docs/PRD.md` | v1.6 — §11.6 corrige o FR-02, §10 revalida o AC, §11.4 registra o caso |
| `docs/diario-de-bordo-sprint.md` | Esta entrada e a do #81 |

### Por que promover fora do ciclo da sprint

A regra do doc de sprint era "`develop` → `main` **uma única vez**, ao final da sprint". O defeito do #81 apareceu **depois** do release, e a regra não dizia o que fazer. A resposta agora está escrita em `docs/sprint-v1-funcional-seguranca.md`, na seção **"Exceção: release de correção crítica fora do ciclo da sprint"** — o critério passa a ser **a maturidade da entrega**, não a data.

O `#81` cumpre as quatro condições: validado end-to-end (rito 8/8 no browser, 63 testes), diff só da correção, CI verde, PR revisado.

E o `main` **não podia ficar como estava**:

- O `main` publicado somava o banco inteiro no card "Vendas Hoje" — o FR-02 do PRD pede o total **do dia**.
- O defeito estava **latente**: o simulador do `main` só gerava o dia corrente, então o número saía certo por coincidência. Ele apareceria no primeiro banco real, que acumula histórico.
- A próxima sprint nasce do `main` ("`develop` é criada a partir de `main` no início da sprint"). Adiar significaria construir a sprint seguinte sobre uma base que promete "Vendas Hoje" e entrega a soma de todos os dias.

### O histórico não é o diff — e por que isso muda a leitura

`git log main..develop` acusava **23 commits**. A leitura ingênua diria "23 commits de trabalho pendente". É o **histórico**, não o trabalho: o release do É7 (#84) foi mergeado com **squash**, achatando 23 commits da entrega num só. O conteúdo que realmente separa `main` de `develop` são 6 arquivos.

É por isso que o release sai com **merge commit**: o squash do #84 escondeu de onde cada mudança veio. A regra "release sempre com merge commit" também foi escrita no doc de sprint.

### Versionamento: as primeiras tags do repositório

O repositório não tinha **nenhuma tag** — "release" era só um ponteiro de branch, sem como citar ou reverter uma versão específica. A primeira tag veio agora, com a semântica `vMAJOR.MINOR.PATCH` documentada no doc de sprint:

| Tag | Aponta para | O que marca |
|---|---|---|
| `v1.0.0` | `932f89a` | Release do É7 — V1 validada no browser. **Retroativa**: nomeia um commit que já existia, sem mover nem reescrever nada |
| `v1.0.1` | merge commit deste release | V1 + a correção do #81 |

Rotular retroativamente o #84 como `v1.0.0` evita que a numeração minta sobre um release anterior que nunca foi rotulado: assim `v1.0.1` é de fato um *patch* sobre uma `v1.0.0` que existe e é verificável.

### O que o release não muda

Nenhuma outra funcionalidade, nenhum commit reescrito, nenhuma issue reaberta. O `main` recebe **merge commit**, os 4 commits do #81 ficam legíveis no histórico, e as tags apontam para o que de fato está publicado.

---

## 🗓️ Quarta, 21/10 (noite, parte 2) — #81: o card "Vendas Hoje" passou a contar só o dia de hoje

> A última dívida que a Fase B deixou de fora. O É7 já estava fechado e o `main` recebera o release; esta correção fecha o que faltava na **semântica** do número, não na sua existência.

### O defeito

O FR-02 do PRD pede o total de vendas **do dia**. A agregação do `/stats` somava o banco inteiro:

```sql
SELECT status, COUNT(*), SUM(valor) FROM transacoes GROUP BY status
```

O card dizia "Vendas Hoje" e mostrava a soma de tudo que estivesse gravado — inclusive de meses atrás.

### Por que ninguém viu (e por que a auditoria não pegou)

Com o banco de referência, as 10 transações são de hoje: o card mostrava o número certo, e o bug ficava **invisível**. A auditoria FR-01..FR-19 marcou **FR-02 "✅ Conforme"** — mas conferiu que o *endpoint* existia, não que o *filtro* existia. É a mesma falha de método da §11.4 com o preflight: a verificação existia, mas cobria o caminho que **já** funcionava.

### A correção

```sql
WHERE date(timestamp) = date('now', 'localtime')
```

Dia civil no fuso do servidor. `date()` aceita tanto `YYYY-MM-DD HH:MM:SS` quanto `YYYY-MM-DDTHH:MM:SS`, então o recorte não depende de como o carimbo de tempo foi gravado.

**O que NÃO foi filtrado:** a tabela "5 últimas transações". Ela mostra as mais recentes de **qualquer** dia — é o que o AC do §10 promete. Filtrar a tabela esconderia do operador justamente o que ele precisa ver: uma transação antiga que deu errado.

**O contrato da API não mudou** (mesmas chaves) e **o frontend não mudou** (zero linha).

### A prova — nos dois sentidos

| Cenário | O card mostra |
|---|---|
| Banco de referência (16 transações, 10 de hoje) | **R$ 803,85** |
| O mesmo banco **sem** o filtro | R$ 1.648,86 (as 4 `CONCLUIDO` de 13, 14, 17 e 19/10 somam R$ 845,01) |
| Com uma transação de ontem de **R$ 5.000,00** injetada | **R$ 803,85** — não se moveu (sem filtro iria a R$ 6.648,86) |

### O simulador ganhou histórico — de propósito

Sem transações de dias anteriores, o recorte seria invisível no produto: o banco só teria movimento de hoje, e o card mostraria o mesmo valor com ou sem o filtro. Uma regressão futura passaria despercebida — exatamente como este bug sobreviveu.

O simulador agora gera **6 transações de 1 a 7 dias atrás**, além das 10 de hoje. As 10 de hoje continuam **idênticas** (mesma semente, mesma ordem de geração, conferido transação a transação): a referência da #67 não mudou — R$ 803,85, 5 concluídas, 3 falhas. `SIMULADOR_HISTORICO` controla a quantidade.

Subtrair no mínimo 1 dia e mais 1 hora garante que nenhuma transação do histórico caia no dia de hoje, mesmo com o simulador rodando perto da meia-noite.

### A bomba-relógio que apareceu no caminho

O fixture de `backend/tests/test_readonly_db.py` criava as transações com a data `2026-10-21` — o dia em que o teste foi escrito. Com o recorte por dia, ele passava só naquele dia e passaria a falhar no dia seguinte. Provado: com o fixture no dia anterior, o teste falha com `assert 0 == 1`.

As datas agora são relativas (meio-dia de hoje), o que também evita a virada da meia-noite.

> **Esse é o tipo de bomba que o recorte criou** — e ela estava lá desde antes, só dormindo. Nenhum teste cobria a passagem do tempo, porque a agregação não dependia do dia.

### Validação

| Gate | Resultado |
|---|---|
| `pytest backend/tests` | **63 passed** (57 + 6 novos do #81) |
| `flake8 backend --select=E9,F63,F7,F82` | **0** |
| `eslint frontend/src` | **0** |
| `npm run build` (dentro da imagem) | ✓ built |
| Rito da #67 repetido | **8/8 ✅** — card R$ 803,85, 4 equipamentos, 15 arquivos 0 ERRO, 8/8 validações `ok`, preflight 200, console limpo |
| Log da API | **0** respostas 403/500 |
| Determinismo do simulador | 2 execuções seguidas → **16 transações idênticas** |

### Gotchas novos

- **O `entrypoint.sh` só roda o simulador se o banco não existir.** Quem já tem `data/abastece.db` precisa apagá-lo para ver o histórico — o `docker compose up` não regenera. Para a validação: `rm data/abastece.db` antes de subir.
- **No console do browser, "Failed to fetch" durante a navegação é artefato.** Abrir outra rota com um fetch em voo aborta a requisição e o `catch` registra o erro. Com 6 s de espera entre rotas, o console fica limpo. A rota das Leitoras é `/leitoras` (sem o "s") — `/leituras` dá aviso de rota inexistente.
- **O adaptador padrão de datetime do sqlite3 foi deprecado na 3.12.** O simulador gravava objetos `datetime` e o Python reclamava a cada inserção. `str(datetime)` escreve exatamente o mesmo formato (`YYYY-MM-DD HH:MM:SS.ffffff`) — trocado, o aviso sumiu e o formato do banco não mudou.

### Estado ao fim

- PRD elevado a **v1.6** — §11.6 corrige o FR-02 (de "Conforme" para "Corrigido"), §10 revalida o AC, §11.4 ganha o bloco do #81
- Branch `feature/epico8-stats-filtro-dia` com 3 commits

---

## 🗓️ Quarta, 21/10 (noite) — Fase B do É7: #67 fechada no browser (8/8 passos, 6/6 ACs)

> A V1 estava "entregue em código" desde 03/10 — e nunca tinha sido olhada. Esta fase pegou o projeto inteiro, montou do zero em container isolado e executou o rito de aceite de verdade. Resultado: **4 dos 8 passos falharam na primeira rodada.** Todos os defeitos passaram pelo build, pelo eslint, pelo pytest e pela CI.

### Entregue (4 correções + a validação)

| Issue | O que era | Correção |
|---|---|---|
| [#78](https://github.com/OsirisMariano/analsita/issues/78) | O botão "Atualizar dados" era um **no-op** | `frontend/src/composables/useRefresh.js` — o evento `analista:refresh` era despachado por `App.vue` e **ninguém escutava** |
| [#79](https://github.com/OsirisMariano/analsita/issues/79) | Categoria `zabbix` sempre com `json_invalido` | O conf do zabbix é um **INI** (`Server=192.0.2.1`), não JSON → a categoria virou `{"tipo": "texto", "padrao": "Server="}` |
| [#80](https://github.com/OsirisMariano/analsita/issues/80) | O banco de referência mudava a cada execução | `SIMULADOR_SEED` (padrão **154622**) + `random.seed()` → 100% reproduzível |
| [#82](https://github.com/OsirisMariano/analsita/issues/82) | A contagem de **falhas** nunca chegava à tela | O `/stats` devolvia `falhas: 3` e o `frontend/src` não tinha **nenhuma** ocorrência da palavra → faltava a linha no card "Vendas Hoje" |

### O dado de referência também estava errado

A #67 esperava **R$ 803,85**. O banco local tinha **R$ 2.320,29** de 24/08/2026 — o simulador gerava números diferentes a cada execução, sem semente. Com `SIMULADOR_SEED=154622`:

- 10 transações: **5 `CONCLUIDO`** somando **R$ 803,85** (é o que o card "Vendas Hoje" mostra), 2 `EM_ABERTO`, 3 `FALHA`
- Total das 10 (contando as 3 falhas): R$ 1.792,81

A referência da #67 **não precisou ser reescrita** — virou verdade. E o banco local foi destruído de propósito (backup em `/tmp/opencode/abastece.db.bak`), com consentimento explícito.

### Validação (container isolado + browser)

| Gate | Resultado |
|---|---|
| `pytest backend/tests` | **57 passed** (53 + 4 de regressão do zabbix) |
| `flake8 backend --select=E9,F63,F7,F82` | **0** |
| `eslint frontend/src` | **0** |
| `npm run build` (dentro da imagem) | ✓ built (1830 modules) |
| **8 passos do rito da #67** | **8/8 ✅** (health, stats, OPTIONS, dashboard, arquivos, navegação, polling, `docker compose up`) |
| Log do container `api` | **88 requisições, todas 200** — nenhum 403, nenhum 500 |
| Console do browser | limpo (só mensagens de debug do Vite) |
| Polling de 5s | 3 ciclos em 13,2 s (2,7 / 7,7 / 12,7 s), todos 200 |
| Badge de erros | provada **nos dois sentidos**: 0 ERRO → badge some; 1 ERRO (mock removido à força) → "Validação de Arquivos 1" |
| Cor do status | conferida no `getComputedStyle`: FALHA `rgb(239,68,68)`, CONCLUIDO `rgb(16,185,129)`, EM_ABERTO `rgb(255,171,0)` |

### Como se prova que a correção do polling funciona

Rodar o código bom e ver que ele funciona **não prova nada** — a falha original era justamente o código "bonito" que não funcionava. Então o teste rodou **duas vezes**:

| Cenário | Ciclos | Intervalos | Sobreposições |
|---|---|---|---|
| Com a guarda `carregando` | 5 | 10,1 / 10 / 10 / 10 s | **0** → `SEM SOBREPOSICAO` |
| Sem a guarda (comentada na hora) | 7 | 5 s × 6 | **5** → `SOBREPOSTO` |

O mesmo método foi usado na #69: três builds da mesma imagem (`--build-arg`, `-e` no runtime, `docker compose build`) mostrando que **sem `ARG`/`ENV` no `Dockerfile` a URL da API não é embutida**.

### Lição

> **Funcionalidade entregue sem verificação observada produz telas que não funcionam.** Nenhum dos 4 defeitos era visível por leitura de código — todos passaram pelo build, pelo eslint, pelo pytest e pela CI. Só apareceram quando alguém olhou a tela rodando.
>
> O espelho da lição de 02/10 (a sprint de segurança consumiu 42 SP e nunca demonstrou a V1 funcionando): a §11.3 já avisava que *hardening* sem verificação end-to-end produz entregas que não rodam. A Fase B mostra que vale para o outro lado também.

### Gotchas novos

- **O CORS padrão do código é `http://localhost:5173`.** Para testar em porta alta (18000/15173) é preciso passar `CORS_ORIGINS` **explícito** no `-e` do container — sem isso o browser toma 403 no preflight e o teste falha por um motivo que não é o do teste.
- **`process.env` do container vence o `.env` do Vite.** Verificado no módulo servido: `http://localhost:18000` apareceu no JS servido, não `http://localhost:8000`.
- **Para medir cor, pegue o elemento certo.** A primeira medição do status pegou o `<td>` (cor padrão) e deu "sem cor". O CSS estava certo, em um `<span class="badge">` dentro da célula.
- **O `frontend/node_modules` local está vazio e com dono root** — build e lint têm que rodar **dentro da imagem** (`docker run --rm -v "$PWD/frontend/src:/app/src:ro" analsita-frontend:latest`).
- **`pytest` e `flake8` não estão em `backend/requirements.txt`** — a CI instala separados. Para rodar local: `pip install pytest flake8` no container.
- **A label `epico-7` não existe**; o MCP do GitHub não tem permissão — usar o `gh` da linha de comando.
- **O fechamento automático de issue por PR não é indexado** neste repositório — as issues precisam ser fechadas à mão, com `gh issue close` e comentário de prova.
- **`docker compose down` não aceita `--rm`** — usar `down -v` quando for preciso remover os volumes.

### Dívidas que saíram desta lista

- ~~Botão "Atualizar dados" não faz nada~~ → **fechado em #78**
- ~~Categoria `zabbix` sempre com `json_invalido`~~ → **fechado em #79**
- ~~Simulador sem semente (banco de referência mudando a cada execução)~~ → **fechado em #80**
- ~~Contagem de falhas ausente no card "Vendas Hoje"~~ → **fechado em #82**
- ~~Falta a confirmação no browser (6 ACs do PRD §10)~~ → **fechado em #67** — os 6 marcados `[x]` com evidência observada

### Dívida que **fica** (de propósito)

- **[#81](https://github.com/OsirisMariano/analsita/issues/81) — `/stats` sem filtro de data.** A API devolve as transações do banco inteiro, sem recorte por dia. Com o banco de referência é invisível; com dados antigos o card "Vendas Hoje" mente. **Não entra neste PR**: mexer na agregação do `/stats` muda a referência de todos os ACs e exige revalidação. Registrada com a V1 já funcional.

### Estado ao fim desta fase

- PRD elevado a **v1.5** — §10 com os 6 ACs `[x]`, §8 com a V1 como "entregue e validada no browser", §11.4 com a tabela dos 8 passos e o que falhou
- Branch `feature/epico7-fase-b-validacao-integrada` com 4 commits de correção (nenhum empurrado ainda)
- É7 fechado: #67 e #62 encerradas, #78/#79/#80/#82 delivered junto do PR

### Publicação

- **PR #83** (`feature/epico7-fase-b-validacao-integrada` → `develop`) mergeado em 21/10 — CI verde nos 3 jobs (backend, frontend, build das imagens)
- **PR #84** (release `develop` → `main`) mergeado em 21/10 — `main` e `develop` com conteúdo idêntico (16 arquivos, +811/−56)
- Issues fechadas à mão (o fechamento automático por PR não é indexado neste repositório): #67, #62, #78, #79, #80, #82
- Board #70 sincronizado: #62, #67, #78, #79, #80, #82 e o PR #83 em `✅ DONE`; **#81 em `📋 BACKLOG`**
- Branch deletada (local e remota); containers isolados derrubados

> O release foi mergeado com **squash** (`932f89a`), enquanto o release anterior (#72) tinha sido merge commit. O conteúdo é o mesmo; a diferença é só no grafo do histórico. Para o próximo release, manter o **merge commit**, que preserva os commits individuais — é o padrão dos PRs de feature do repositório.

---

## 🗓️ Quarta, 21/10 (tarde) — Bloco 2 do É7: #74 e #75 entregues



> Continuação do mesmo dia. Duas das três dívidas registradas abaixo no Bloco 1 foram fechadas. Branch nova, empilhada sobre `feature/epico7-polling-e-mocks` (que segue **sem push**): `feature/epico7-readonly-e-env-fallback`.

### Entregue (2 de 7 tasks do É7)
- ✅ **#74 (T8) — banco SQLite em modo somente-leitura** → `backend/app/main.py` + `backend/tests/test_readonly_db.py`
- ✅ **#75 (T9) — frontend sem depender de `.env` não versionado** → `frontend/src/api.js` + `frontend/.env.example`

### O que foi feito

**#74 — a API não escreve no banco (e agora isso é garantido, não convenção)**

O PRD §7 exigia que a API não escrevesse, mas a garantia era só do código: as rotas faziam `SELECT` e nada impedia uma escrita acidental. A conexão passou a ser aberta com `mode=ro` na URI, que faz o **próprio motor do SQLite** recusar qualquer escrita (`attempt to write a readonly database`).

O mount de `./data` **continua gravável de propósito**: o `entrypoint.sh` precisa criar o banco quando ele ainda não existe, e um diretório somente-leitura impediria isso. A garantia que importa foi posta no lugar certo — dentro do programa. O isolamento de filesystem (`:ro` no mount) segue fora do escopo da V1.

**#75 — o painel funciona sem nenhum arquivo local**

O `frontend/.env` cai na regra `.env` do `.gitignore` da raiz e nunca foi versionado. Quem clonava o repositório recebia o frontend sem configuração e o painel não carregava (`fetch("undefined/stats")`). Agora:

- `frontend/src/api.js` é a **fonte única** da URL: usa `VITE_API_URL` quando ela existe e cai para `http://localhost:8000` quando não existe. O `store.js` e a `HomeView.vue` leem a URL de lá — antes cada um repetia a definição.
- `frontend/.env.example` entra no repositório (não é ignorado pelo `.gitignore`, confirmado com `git check-ignore`), documentando a configuração como **opcional**.

### Validação (gate local + container real + browser)

| Gate | Resultado |
|---|---|
| `pytest backend/tests` | **53 passed** (50 + 3 novos) |
| `flake8 backend --select=E9,F63,F7,F82` | **0** |
| `npm run build` (dentro da imagem) | ✓ built (1829 modules) |
| Bundle gerado | contém `http://localhost:8000` e **0 ocorrências** de `undefined/stats` |
| `docker compose config` | válido |
| Container real — escrita pela API | **recusada**: `attempt to write a readonly database` |
| Container real — escrita pelo simulador | **ok** (o mount segue gravável) |
| Container real — `/transacoes` e `/stats` | 200, e o **hash e a data do banco não mudaram** |
| Container real — `PRAGMA database_list` | `/var/abastece/dados/abastece.db` (caminho normal, sem alteração) |
| **Browser sem o `frontend/.env`** | painel carrega com dados, console limpo, `GET /stats` → 200 e `GET /monitoramento` → 200 (antes: `undefined/stats` e erro no console) |
| Browser — Validação de Arquivos | 15 linhas, **0 ERRO** |
| Browser — Validação de Dados | tudo `ok`, **menos** o `zabbix` (dívida preexistente, ver Bloco 1) |

### Prova de que o teste pega a regressão

O teste foi rodado **com a correção removida** (`sqlite3.connect(DB_PATH)` sem `mode=ro`): **2 dos 3 testes falham** (`test_conexao_rejeita_escrita` e `test_conexao_usa_uri_readonly`). Sem o `mode=ro`, o conjunto passa a falhar — o teste prende o contrato, não só o efeito.

> `test_api_nao_altera_o_banco` **passa** mesmo sem a correção — ele prova o comportamento (as rotas leem e não mexem no arquivo), não a garantia. A garantia é dos outros dois.

### Gotcha novo

- O `gh issue create` com o rótulo `epico-7` **falha**: o rótulo não existe no repositório. Os rótulos em uso no É7 são `frontend`, `backend`, `infra/docker`, `epic`, `security`, `bug`.
- O MCP do GitHub (`github_create_issue`) retorna `Resource not accessible by personal access token` — **use o `gh` da linha de comando** para criar issues.

### Dívidas que saíram desta lista
- ~~`frontend/.env` não versionado derruba o AC do PRD §10~~ → **fechado em #75**
- ~~SQLite não é read-only (PRD §7)~~ → **fechado em #74** (no código; o isolamento de filesystem segue fora do escopo)

### Dívidas que continuam
- `scripts/simulador_posto.py` é **aleatório** → os números de referência da #67 não se reproduzem em clone limpo. Fix proposto: `random.seed()` fixo.
- Categoria `zabbix` em `validacoes_config.py:81` (preexistente) — o PO decidiu **abrir issue e corrigir junto**; ainda não feito.
- **Fase B da #67** (latência induzida para provar o #65, e grep do bundle para provar o #69).

### Publicação no GitHub (21/10, fim do dia)
- **PR #76** → `develop`, **mergeado** (`be6a8ee`). As duas branches foram empilhadas e subiram juntas, num PR só.
- CI do PR: **Backend CI, Frontend CI e build das imagens — todos verdes**.
- Issues **#65, #66, #68 e #69 fechadas** com o comentário da prova. A **#64** também foi fechada agora: a entrega era de 03/10 (PR #73) e só faltava o registro. A **#67** fica aberta — é a Fase A (browser) e a Fase B.
- #74 e #75 criadas, fechadas e **colocadas no board #70**.
- Board #70 atualizado: #63, #64, #65, #66, #68, #69, #74, #75 em **✅ DONE**; #62 (épico) em **🔨 IN PROGRESS**; #67 em **📥 TO DO**; backlog de segurança (#51–#55) intacto em **📋 BACKLOG**.
- Issues do É7 com **responsável** (`OsirisMariano`) e **milestone É7** preenchidos.

> **Gotcha:** o fechamento automático por PR **não funcionou** neste repositório. As linhas `Closes #65`…`Closes #75` estão no corpo do PR e o GitHub cria a referência cruzada (aparece no histórico de cada issue), mas o `closingIssuesReferences` fica vazio — testei com uma issue nova e descartável e o resultado foi o mesmo. As issues foram fechadas **manualmente**, com `gh issue close` e o comentário da prova, que é o que já se fazia com a #63, a #74 e a #75. **Não confiar no fechamento automático ao fechar a #67.**

> **Outro gotcha:** o `gh issue create --label "epico-7"` falha — o rótulo não existe. Os rótulos em uso no É7 são `frontend`, `backend`, `infra/docker`, `epic`, `security`, `bug`, `documentation`.

---

## 🗓️ Quarta, 21/10 — Épico 7: #65, #66 e #69 entregues

### Entregue (3 de 7 tasks do É7)
- ✅ **#65 (T3) — FR-03: polling sem sobreposição** → `HomeView.vue`
- ✅ **#66 (T4) — mount `var/DS_SFTP`** → `docker-compose.yml` (diagnóstico do "13/15 em ERRO" incluído)
- ✅ **#69 (T7) — remover `build.args` morto** → `docker-compose.yml`
- Branch: `feature/epico7-polling-e-mocks` (a partir de `develop` @ `b75c02a`)

### O que foi feito

**#65 — polling sem sobreposição**
- `carregando` (ref) como guarda: `carregarDados` retorna cedo se a requisição anterior está em voo
- `finally` libera a guarda — um erro na API não trava o loop
- `clearInterval` no `onUnmounted` (antes o timer vazava a cada troca de rota)
- `onMounted` guarda o id do intervalo em `intervalo`

**#66 — mount `mock_data/var/DS_SFTP`**
- **Diagnóstico:** os "13 de 15 em ERRO" medidos pelo PO em 01/10 eram **artefato do ambiente de medição**. A API foi medida no host (porta 8899), onde os caminhos de container não existem — só `/etc/hosts` e `/etc/hostname` batem, exatamente 2 → 13 ERROS. Dentro do container o `mock_data` cobre 14 dos 15.
- **Lacuna real:** `mock_data/var/DS_SFTP/config.json` existia mas `./mock_data/var/DS_SFTP` **não estava montado** → `config.json` ERRO em `/arquivos` e a categoria `config` (SFTP_SERVER) quebrada em `/validacao-dados`.
- **Fix:** 1 linha de mount. Resultado: `/arquivos` → **15/15 OK, 0 ERRO**; `config` voltou a `ok`.

**#69 — `build.args` morto**
- Removido o bloco `args: VITE_API_URL: http://api:8000` do serviço `frontend`. O `frontend/Dockerfile` nunca declarou `ARG`, então era ignorado — e virava armadilha: declarar o `ARG` embutiria o hostname **interno** `api` no bundle, quebrando o browser com DNS error em produção (e só depois do deploy).

### Validação (gate local)

| Gate | Resultado |
|---|---|
| `pytest backend/tests` | **50 passed** (venv via `uv` em `/tmp/opencode`, py3.11) |
| `flake8 backend --select=E9,F63,F7,F82` | **0** |
| `npm run build` (dentro da imagem) | **✓ built in 3.56s** (1828 modules) |
| `docker compose config` | válido, sem `VITE_API_URL` |
| Container real (`docker compose up -d api`) | `/health` 200 · `/arquivos` 0 ERRO · `/stats` 4 disp., 4 concl., 3 fal., **R$ 803,85** · `OPTIONS /stats` 200 |

> Números de `/stats` batem **exatamente** com a referência do PO na #67 (R$ 803,85 / 10 transações / 4 dispositivos).

### Gotcha novo

- `frontend/node_modules` local está **vazio e é root-owned** → `npm run build` na host falha com `vite: not found`. Workaround: `docker build -t analsita-frontend:validate ./frontend && docker run --rm analsita-frontend:validate npm run build` (mesmo caminho da CI, sem sujar a host).
- `docker compose down` **não aceita `--rm`** nesta versão (v5.5.0) — use `docker compose down -v`.

### Achado novo **fora** do backlog (abrir issue)

- **`/validacao-dados` → categoria `zabbix` retorna "1 erro(s)"** — preexistente, não introduzido aqui. A regra em `validacoes_config.py:81` valida `/etc/zabbix/zabbix_agent2.conf` com `tipo: json_valor`, mas o arquivo é **INI** (`Server=192.0.2.1`), não JSON → `json.loads` falha → `json_invalido`. Correção provável: trocar por `{"tipo": "texto", "padrao": "Server="}`.

### Restante do É7

- **#67 (T5) — validação integrada `docker compose up`** ← **próximo e é o que fecha a V1**: 8 passos, incluindo o browser (dashboard, badge, navegação, console, 2 ciclos de polling). Regra do PRD §10: só marcar `[x]` com evidência observada no browser.
- **#68 (T6)** — entregue na substância (PRD v1.3 + esta entrada); falta apenas fechar a issue.
- **#63, #64** — entregues, issues ainda abertas. Fechar.
- **#66, #69, #65** — fecham com este PR.
- Backlog sem prazo: #52 (TLS), #53 (login), #54 (rate limit), #55 (logging estruturado).

### Dívidas conhecidas (fora do É7)

- ~~`frontend/.env` **não é versionado** (cai no `.env` do `.gitignore` da raiz) → em clone limpo o frontend sobe sem `VITE_API_URL` e faz `fetch("undefined/stats")`. Derruba o AC do PRD §10 *"Toda a solução sobe com `docker compose up`"*.~~ → **FECHADO no Bloco 2 do mesmo dia (#75).**
- ~~**SQLite ainda não é read-only** (PRD §7 RNF): `docker-compose.yml:18` monta `./data` sem `:ro`. Decisão do PO em 21/10: read-only **no código** (`mode=ro` na URI do `sqlite3.connect`), mantendo o mount gravável porque o `entrypoint.sh` precisa escrever o banco quando ele não existe.~~ → **FECHADO no Bloco 2 do mesmo dia (#74).**
- `scripts/simulador_posto.py` é **aleatório** → os números de referência da #67 não se reproduzem em clone limpo. Fix proposto: `random.seed()` fixo.

---

## 🗓️ Quinta, 10/09 — Épico 4 entregue · board sincronizado

### Entregue (5 de 6 épicos)
- ✅ **Épico 4 — Error Handling** → PR #60 merged na develop (1 commit `555638e`: SEC-18..21)
- Issues fechadas: #36, #37, #38, #39 + épico pai **#16**

### O que foi feito (SEC-18..21)
- `SEC-18` — `/transacoes` devolve 500 `"Erro interno ao acessar o banco de dados"` (era `f"Erro ao ler banco: {str(e)}"`)
- `SEC-19` — `/validacao-dados` envolto em `try/except` → 500 genérico + `print()` server-side
- `SEC-20` — `extrair_valor()` retorna `"erro_leitura"` puro (era `f"erro_leitura: {e}"`); detalhe só no `print()`
- `SEC-21` — auditoria: únicos `str(e)` expostos eram os corrigidos; `print` de `/stats` permanece server-side

### Bônus: synchronizei o board
- Board estava todo na coluna errada: **É1 (#13, #19–23) e É5 (#17, #40–44)** ainda em TO DO apesar de mergeados → movidos 12 cards para **DONE**
- Issue **#13 (Épico 1)** estava OPEN (Closes só fecha na main) → fechada manualmente via `gh issue close`
- Cards do É4 (#16, #36–39) seguiram o ritual: IN PROGRESS → CODE REVIEW → MERGE→develop → DONE

### Validação (gate + ponta a ponta no container)
- **21 testes pytest verdes** (18 antigos + 3 novos em `tests/test_error_handling.py`) + flake8 limpo
- CI 3/3 checks passando (Backend, Frontend, Docker Build)
- No container real: `/transacoes` e `/validacao-dados` → 200 no fluxo normal; código deployado com mensagens genéricas (grep); corpo sem `erro_leitura:` com detalhe
- Gotcha prático: nesta máquina não há pytest no python3 → usei venv em `/tmp/opencode` via `uv` (mesma versão do CI)

### Restante da sprint (prazos vencidos)
- **Épico 6 — Frontend Produção** (#45–49, prazo 31/08) — último, muda runtime do frontend
- Backlog futuro (#51–55): fora desta sprint
- Fim: release PR `develop → main` → épico vai para produção

---

## 🗓️ Quarta, 09/09 — Épico 1 entregue

### Entregue (4 de 6 épicos)
- ✅ **Épico 1 — CORS + Autenticação** → PR #59 aberto na develop (`feature/cors-auth`)
- Commits: `4066527` (SEC-01..05) + `efaaa42` (httpx como dep de teste)
- Issues cobertas: **#19, #20, #21, #22, #23** — **aguardando aprovação do PO no PR #59** (não mergeado ainda)

### O que foi feito (SEC-01..05)
- `SEC-01` — `allow_origins` restrito via env `CORS_ORIGINS` (default `http://localhost:5173`)
- `SEC-02` — `allow_methods=["GET"]` (antes `["*"]`)
- `SEC-03` — Middleware `ApiKeyMiddleware` → **403** sem header `X-API-Key` válido (compara com `hmac.compare_digest`)
- `SEC-04` — `API_KEY` lida de env var (fallback dev `dev-key-not-secure`)
- `SEC-05` — `.env.example` consolidado (`CORS_ORIGINS` + `API_KEY`)
- Rotas isentas da chave: `/health`, `/docs`, `/openapi.json`, `/redoc`

### Validação (gate + ponta a ponta no container)
- **18 testes pytest verdes** (13 antigos + 5 novos em `tests/test_seguranca.py`) + flake8 (E9,F63,F7,F82) limpo
- CI 3/3 checks passando (Backend, Frontend, Docker Build)
- No container real: sem chave → `403` · chave errada → `403` · chave válida → `200` · `/health` → `200`
- CORS: origin `localhost:5173` retorna `access-control-allow-origin`; origin externa **não** recebe header

### Gotchas novos acumulados
- `TestClient` do starlette/FastAPI 0.109 **exige `httpx` explicitamente** → adicionado `httpx==0.24.1` ao `backend/requirements.txt` (CI fail `ModuleNotFoundError: httpx` na 1ª tentativa)
- **Pra não quebrar o TestClient antigo**: fixar `httpx==0.24.1` (versão recente quebra com `unexpected keyword argument 'app'`)
- `JSONResponse` usa `content=`, **não** `detail=` (esse é próprio do `HTTPException`)
- ⚠️ Frontend agora precisa enviar o header `X-API-Key` em toda request, e `allow_headers` baixou para `["X-API-Key"]` — pode quebrar chamadas que antes passavam sem chave

### Restante da sprint (prazos vencidos)
- **Épico 4 — Error Handling** (#36–39, prazo 28/08) ⚠️ depende do É1 — **próximo** (assim que o PR #59 for mergeado)
- **Épico 6 — Frontend Produção** (#45–49, prazo 31/08) — último, muda runtime do frontend
- Backlog futuro (#51–55): fora desta sprint
- Fim: release PR `develop → main` → épico vai para produção

---

## 🗓️ Sábado, 05/09 — Retomada: Épico 5 entregue

### Entregue (3 de 6 épicos)
- ✅ **Épico 5 — Configuração + Segredos** → PR #58 merged na develop (1 commit `cca0d97`: SEC-22..26)
- Issues fechadas: #40, #41, #42, #43, #44 + épico pai **#17**

### O que foi feito (SEC-22..26)
- `SEC-22` — `EQUIPAMENTOS` lido de env var JSON com fallback (`backend/app/main.py`)
- `SEC-23` — `DB_PATH` lido de env var com fallback
- `SEC-24` — `CONVENIADO_CODE`, `SFTP_SERVER`, `NUC_IP` via env (`backend/app/validacoes_config.py`)
- `SEC-25` — IP do Zabbix mock → `192.0.2.1` (RFC 5737) em `mock_data/etc/zabbix/zabbix_agent2.conf`
- `SEC-26` — criado `backend/.env.example` (placeholders, sem valores reais)
- `docker-compose.yml` — serviço `api` injeta `backend/.env` com `required:false` (sobe mesmo sem o arquivo, usando fallbacks)

### Validação (gate + ponta a ponta no container)
- 13 testes pytest verdes + flake8 limpo + CI 3/3 checks passando (Backend, Frontend, Docker Build)
- **Sem `.env`** → fallbacks: 4 equipamentos fixos, 02896 / DS_ABAST.02896_1 / 192.168.212.21
- **Com `.env`** → `/monitoramento` e `/validacao-dados` refletem os overrides (ex: 2 equipamentos, 7777 / DS_ABAST.7777_1 / 10.10.10.10)
- `.env` real ignorado pelo `.gitignore`; apenas `.env.example` versionado

### Gotchas novos acumulados
- `env_file` com `required:false` (compose ≥2.24) deixa o compose subir sem o `.env` — ideal para fallbacks
- Para as env vars surtirem efeito no container, o compose precisa injetá-las (`env_file`); o Dockerfile por si só não expõe `EQUIPAMENTOS`/segredos
- Branch feature deletada em seguida do merge (local + remota) — retomar a partir de `develop`

### Restante da sprint (prazos todos vencidos)
- **Épico 1 — CORS + API Key** (#19–23, prazo 27/08) — Ó próximo, par urgente (rodar após o É5: mesmos arquivos)
- **Épico 4 — Error Handling** (#36–39, prazo 28/08) ⚠️ depende do É1
- **Épico 6 — Frontend Produção** (#45–49, prazo 31/08) — último, muda runtime do frontend
- Backlog futuro (#51–55): fora desta sprint
- Fim: release PR `develop → main` → épico vai para produção

---

## 🗓️ Terça, 25/08 — Fila do dia (preparada na segunda)

### Sequência planejada
1. **Épico 5 — Configuração + Segredos** → branch `feature/config-secrets`
2. PR → merge na develop
3. **Épico 1 — CORS + API Key** → branch `feature/cors-auth` (rodar APÓS o É5: mesmos arquivos)
4. PR → merge na develop

Ambos com prazo **27/08** — são o par urgente da sprint.

### Ordem das tasks

**É5 (8 SP):**

| Ordem | Task | Issue | O que é |
|---|---|---|---|
| 1º | SEC-22 | #40 | Externalizar `EQUIPAMENTOS` (env JSON + fallback) |
| 2º | SEC-23 | #41 | Externalizar `DB_PATH` |
| 3º | SEC-24 | #42 | Externalizar `CONVENIADO_CODE`, `NUC_IP`, `SFTP_SERVER` |
| 4º | SEC-25 | #43 | IP do Zabbix mock → RFC 5737 (`192.0.2.1`) |
| 5º | SEC-26 | #44 | Criar `.env.example` do backend (documenta todas as vars) |

**É1 (8 SP):**

| Ordem | Task | Issue | O que é |
|---|---|---|---|
| 1º | SEC-01 | #19 | CORS `allow_origins` restrito |
| 2º | SEC-02 | #20 | CORS `allow_methods=["GET"]` |
| 3º | SEC-04 | #22 | Variável `API_KEY` no ambiente |
| 4º | SEC-03 | #21 | Middleware API Key (403 sem header válido) |
| 5º | SEC-05 | #23 | `.env.example` consolidado (`API_KEY` + `CORS_ORIGINS`) |

### Ritual fixo por task
Card IN PROGRESS + assignee OsirisMariano → implementar → validar local → card CODE REVIEW → PO aprova → cards MERGE→develop → PR com `Closes #N` → merge → fechar issues manualmente → cards DONE.

---

## 🗓️ Segunda, 24/08 — Primeiro dia da sprint

### Entregue (2 de 6 épicos, ambos com folga no prazo)
- ✅ **Épico 3 — Docker Hardening** → PR #56 merged na develop (9 commits: SEC-10..17 + SEC-32)
- ✅ **Épico 2 — Validação de Input** → PR #57 merged (4 commits: SEC-06..09)
- Issues fechadas: #13, #14, #15 e as 13 tasks · Cards em DONE
- CI agora roda **pytest real como gate** (removido o `|| echo` que engolia falhas)

### Estado técnico atual
- `develop` @ merge do PR #57 · branch `main` congelada até o fim da sprint
- Containers rodando com imagens novas (non-root: api=appuser, web=node; NET_RAW; código read-only; sem --reload)
- Suíte: 13 testes pytest verdes (`backend/tests/`)
- `data/` já com dono 1000:1000 (feito manualmente pelo PO via sudo)

### Pendências administrativas do PO (GitHub UI, ~5 min)
- [ ] View Board agrupada por Status no Project #70
- [ ] Ativar automações nativas do Project
- [ ] Instanciar iteração do campo Sprint (início 24/08, duração 7 dias)

### Lições/gotchas acumulados (não redescobrir!)
- `.dockerignore` é lido da raiz do **contexto** de build, não do repo (por isso existem 3 arquivos)
- `Closes #N` só fecha issue se o merge for para a branch **default** (main); na develop fechamos manualmente
- Push de feature branch não dispara CI — só PR ou push em develop/main
- Sem `--reload`: mudança de código exige `docker compose restart api`
- `npm install` como não-root exige `/app` com dono correto antes do `USER`
- Imagem `node` já traz usuário `node` uid 1000 — reutilizar, não duplicar
- Validar sempre em container isolado (`--rm`, porta alta) antes de commitar

### Restante da sprint (após amanhã)
- Épico 4 — Error Handling & Logs (#36–39, prazo 28/08) ⚠️ depende do É1
- Épico 6 — Prod build Frontend (#45–49, prazo 31/08) — último, muda runtime do frontend
- Backlog futuro (#51–55): fora desta sprint
- Fim: release PR `develop → main` → épico vai para produção

---

## 2026-10-01 → 2026-10-02 — Reclassificação e correção do PRD (#62, #68)

### Decisões do PO (01/10)
O projeto foi reclassificado como **projeto de estudos**. Consequência direta: **segurança sai do caminho crítico**.
Autenticação fora da V1 (#63 torna a API key opt-in) · CORS segue restrito · Épico 6 (build prod) cancelado ·
#52/#53/#54/#55 vão para backlog sem prazo · FR-03 corrigido (#65).

### Por que essa entrada existe
A sprint de segurança consumiu **42 SP**, entregou 5 de 6 épicos — e a V1 funcional **nunca foi demonstrada funcionando**.
O painel está vazio desde 09/09 porque toda chamada do frontend à API retorna **403**.

**Causa raiz = duas linhas:**
1. O frontend não envia `X-API-Key` (0 ocorrências em `frontend/src`) → #63
2. `ApiKeyMiddleware` (`main.py:41`) não isenta `OPTIONS` e é a camada mais externa, então mata o preflight → #64

**Por que a CI ficou verde:** `TestClient` não simula preflight CORS. O teste que falta é o de preflight (DoD do #64).

### Correção do PRD (02/10, #68)
PRD elevado a **v1.2**. Divergências corrigidas contra o código:
- **FR-19** reescrito: allowlist `CORS_ORIGINS` + `X-API-Key` obrigatório. A redação antiga ("CORS de qualquer origem") estava obsoleta desde o PR #59.
- **FR-11** corrigido: a lista de arquivos vive em `backend/app/arquivos_config.py` (15 entradas), não em `store.js`.
- **RNF SQLite read-only** corrigido: `docker-compose.yml:18` monta `./data` **sem `:ro`** — o requisito não é garantido pela infra (#67).
- **Roadmap V1 decidido**: "integração dos dados de validação via API" já estava implementada (marcada como pendente por engano); "configuração dinâmica" migrou para a V2.
- **Nova §11** registra a reclassificação, o bloqueio atual e a auditoria FR-01..FR-19.

**Resultado da auditoria:** nenhum requisito da §6 falta no código. 14 conformes, 2 mockados por escopo, 1 parcial (#65).
O bloqueio é de **integração**, não de implementação.

### Regra permanente (nasceu deste episode)
> Toda task que altera comportamento observável atualiza o PRD no mesmo PR.

Já estava escrito desde a v1.0 ("documento vivo") e não foi cumprido. A divergência do FR-19 custou a §11 inteira.

### Lição
Segurança aplicada sem verificação end-to-end gera entrega que não sobe. O epic de segurança passou 5/6 e mesmo assim
entregou um painel que não abre no browser. **Antes de promotes código para `main`, rodar o fluxo real no browser** —
a CI verde não cobre preflight CORS nem integração frontend↔backend.

### Próximos passos
`develop` → `main` promovido em 02/10 (26 commits, incluindo SEC-01..32).
Basta #63 + #64 (4 SP) para a V1 ficar demonstrável.
