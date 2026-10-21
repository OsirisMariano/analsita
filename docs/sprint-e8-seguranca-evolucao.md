# Sprint É8 — Segurança & Evolução

> **Status:** Planejado pelo PO em 21/10/2026. **Aguardando execução** — nenhuma task deste documento foi iniciada.
> **Milestone:** [É8 — Segurança & Evolução](https://github.com/OsirisMariano/analsita/milestone/8) · **Janela:** 26/10/2026 → 06/11/2026
> **Base:** PRD v1.6 §5.2, §7, §8, §11.1–11.5 · sprint anterior `docs/sprint-v1-funcional-seguranca.md` · código em `develop` (`d5e72e9`)
> **Issues:** [#51](https://github.com/OsirisMariano/analsita/issues/51) · [#52](https://github.com/OsirisMariano/analsita/issues/52) · [#53](https://github.com/OsirisMariano/analsita/issues/53) · [#54](https://github.com/OsirisMariano/analsita/issues/54) · [#55](https://github.com/OsirisMariano/analsita/issues/55)

---

## 1. O problema que vamos resolver

**Em uma frase:** hoje o painel é aberto para quem alcança a porta, e o É8 fecha a porta com chave, mantém a fechadura de quem entra e deixa rastro de quem passou.

**A analogia:** o painel de hoje é um galpão com a porta encostada. O `X-API-Key` (FR-19) é uma corrente no portão — mas ela só existe se alguém a pendurar, e **ninguém pendura**. Não há lista de quem pode entrar, não há limite de quantas vezes se pode bater na porta, e não há registro de quem bateu. O É8 não é um cofre: é **a fechadura, o cartão de acesso, a placa de "não bata mais que 20 vezes" e o livro de ponto** de um galpão que já tem mercadoria dentro.

**Por que agora, e não antes:** o PRD §11.2 classifica essas pendências como *"backlog sem prazo — reescritos quando as funções estiverem definidas"*. A função da V1 agora **está** definida e observada no browser (a #67 provou isso em 21/10). Endurecer a porta antes de o painel ser confiável é erguer parede em casa sem chão.

**Por que agora, e não depois:** o §11.3 registra o preço de errar a ordem — 42 SP de hardening enquanto a V1 nunca foi demonstrada funcionando. O É8 inverte a ordem: **cada épico fecha com o painel verificado, não o sprint inteiro**.

---

## 2. Decisões do PO (D1–D5)

As cinco issues do É8 foram escritas como pendências soltas em 01/10/2026. Para planejar, elas precisavam de decisões que não cabem no texto de uma issue. Todas as cinco estão aqui, com o motivo — porque a §11.2 do PRD exige exatamente isso: reescrever a função **antes** de estimar.

| # | Decisão | Escolha | Por quê | Custo se fosse diferente |
|---|---|---|---|---|
| **D1** | Onde fica a identidade dos usuários? | **SQLite separado (`auth.db`)**, gravável, criado pelo `entrypoint.sh` | A API abre o banco de transactions com `mode=ro` (§7, RNF "Acesso ao banco") — ela **não pode gravar** uma tabela de usuários no mesmo arquivo. Um banco separado é a solução que não exige reescrever a garantia de leitura-only | OIDC exigiria um provedor de identidade externo; a §11.1 diz que não há operação contínua nem rede de produção. Seriam ~10 SP a mais e uma dependência que o projeto de estudos não tem |
| **D2** | Onde fica o rate limit? | **In-process**, no FastAPI (chave por IP/cliente) | Mantém a #54 **independente** da #52 e permite as ondas em paralelo. `limit_req` do nginx seria a opção "correta" em produção, mas aqui amarraria a #54 à #52 — a onda mais pesada | `limit_req` custaria +1 SP, mas serializaria as ondas 2 e 3 |
| **D3** | A #52 (TLS) entra na execução do É8? | **Sim no escopo, mas na Onda 3 — a última, e a única dispensável.** A recomendação do PO é **transferir a execução para a V2** | Certificado self-signed, sem domínio, sem cliente e sem operação contínua (§11.1) é **teatro com o custo mais alto do lote**. E é a issue que mais pode quebrar a V1: muda CORS, muda a URL da API e mexe no preflight | TLS real (Let's Encrypt) exige domínio — fora do alcance de um projeto de estudos |
| **D4** | O escopo de papéis (roles) entra? | **Não.** O É8 entrega **identidade + 1 nível** (`admin` / leitura) | A matriz `analista/supervisor/admin` é item da **V2** (§8). E papel sem tela para usá-lo é código morto. A #55 só precisa de *um* identificador de quem acessou | 3 SP de matriz de papéis, sem valor observável |
| **D5** | Quando o É8 fecha? | **06/11/2026**, começando em 26/10/2026 | 7 dias úteis cobrem a Onda 1 + Onda 2 (49 SP). Com a Onda 3 inteira, são 8,5 dias — a data serve para os dois cenários | — |

> **D3 em uma frase:** a #52 **fica** no milestone É8 (tirar de lá a transformaria em issue órfã — exatamente o problema que a hygiene de board acabou de resolver). O que muda é a **ordem**: ela é a última onda, e a recomendação do PO é executá-la na V2, registrando a transferência no §8 do PRD. **O milestone fecha com 4 issues entregues e a #52 condicionada, ou com 5 — a decisão se toma no fim da Onda 2, com o time.**

---

## 3. O que será construído (5 épicos)

**Plano (sem jargon, para quem nunca leu o código):** cada épico abaixo tem uma frase que explica o resultado, a lista de tasks com o critério de aceite, e os story points. O critério de aceite de toda task que muda comportamento observável passa pelo **rito de 8 passos** da §10.

### Épico 1 — #51 · Dados sensíveis fora do versionamento · **6 SP**

> **O que é:** garantir que o repositório nunca guarde credencial de verdade. Hoje ele não guarda nenhuma — os 19 arquivos de `mock_data/` são placeholders ("mock license data", `Server=192.0.2.1`). O trabalho real é **erguer a cerca antes que alguém traga a senha da loja**.

| ID | Task | Critério de aceite | SP |
|---|---|---|---|
| É8-01 | Auditar os 19 arquivos de `mock_data/` e **declarar** a lista de sensíveis por definição (licença, certificado, `posto.json`, `concentrador.json`) | Relatório versionado: 19 arquivos, 0 segredo real, 3 IPs de LAN em 7 mocks | 1 |
| É8-02 | Remover do git os sensíveis (`git rm --cached`) e declará-los no `.gitignore` | `git ls-files mock_data` não lista nenhum arquivo da lista sensível | 1 |
| É8-03 | Substituir por fixtures **genéricas** que preservem a validação | `GET /arquivos` continua retornando **15 arquivos, 0 ERRO** (§11.4) | 2 |
| É8-04 | Escrever a regra "nunca versionar" no doc do sprint + `.gitignore` comentado | Regra versionada e legível | 1 |
| É8-05 | Atualizar o PRD no mesmo PR (§11.5) | PRD atualizado | 1 |

> **Por que o histórico do git não é reescrito:** não há segredo real no histórico, então reescrever custaria as tags `v1.0.0`/`v1.0.1` sem comprar nada. Se um dia entrar um segredo real, a providência passa a ser **rotacionar o segredo** — e não reescrever o histórico. A regra está escrita na É8-04.

### Épico 2 — #53 · Autenticação real (login/senha) · **20 SP** · peça central

> **O que é:** trocar a corrente no portão por uma **porta com fechadura**. Quem abre precisa de usuário e senha; a API passa a saber **quem** é a pessoa, não só se a requisição tem um carimbo.

| ID | Task | Critério de aceite | SP |
|---|---|---|---|
| É8-11 | Decisão de identidade: store, algoritmo de hash, formato e validade do token | ADR curto neste doc | 1 |
| É8-12 | Criar `auth.db` **separado** (a API é `mode=ro` no banco de transactions) com tabela `usuarios` + seed | Schema criado pelo `entrypoint.sh`; 1 usuário admin | 3 |
| É8-13 | `POST /auth/login` — verifica hash, emite token de curta duração | Token válido; senha errada → **401** genérico (sem dizer qual campo falhou) | 3 |
| É8-14 | Middleware de autenticação + rotas isentas (`/health`, `/docs`, `/openapi.json`, `/redoc`, login) + **`OPTIONS` isento por método** | O preflight responde **200** — não repetir o bug do §11.4 | 3 |
| É8-15 | Frontend: tela de login + injeção do token em `api.js` (fonte única da URL) | `api.js` passa a enviar a credencial | 3 |
| É8-16 | **Modo opt-in por env** (`AUTH_ENABLED`), espelhando o padrão da #63 | Sem `AUTH_ENABLED`, a API se comporta exatamente como hoje | 3 |
| É8-17 | Testes: login ok · senha errada · token expirado · rota isenta · preflight · modo off | Os 6 cenários cobertos | 3 |
| É8-18 | Atualizar FR-19 no PRD + §10 | PRD no mesmo PR (§11.5) | 1 |

> **O porquê do modo opt-in:** é o **mesmo padrão que a #63 já provou** para a API Key (opt-in, `API_KEY` ausente = sem credencial). O motivo não é segurança — é **não repetir a §11.4**: se a autenticação virar obrigatória e o frontend não souber falar com ela, o painel inteiro quebra. O opt-in permite rodar o rito **nos dois modos**: com e sem autenticação.

### Épico 3 — #55 · Logging estruturado e auditoria · **12 SP**

> **O que é:** trocar o papelote ("deu erro") por um **livro de ponto**: cada requisição vira uma linha estruturada com quem fez, de onde veio, quanto tempo levou e o que respondeu. E a **trilha de auditoria** guarda o rastro dos endpoints sensíveis.

| ID | Task | Critério de aceite | SP |
|---|---|---|---|
| É8-25 | Logging estruturado em JSON (formatter próprio sobre `logging` da stdlib — **zero dependência nova**) | 100% das linhas em JSON, com `level` | 3 |
| É8-26 | Middleware de `request-id` (gera ou propaga `X-Request-ID`) | 100% das requisições com id no log | 2 |
| É8-27 | Trilha de auditoria nos endpoints sensíveis (`/auth/login`, `/stats`, `/monitoramento`, `/arquivos`), **com usuário quando houver** | Entrada com `usuario`, `ip`, `status`, `duracao_ms` | 3 |
| É8-28 | **Redação de segredos**: senha e token nunca no log | Teste automatizado que **falha** se vazar | 2 |
| É8-29 | Trocar os 4 `print()` de `backend/app/` por logging com nível | 0 `print()` em `backend/app/` | 1 |
| É8-30 | Atualizar o RNF de Observabilidade (§7) | PRD atualizado | 1 |

> **Por que a auditoria vem depois da #53:** uma trilha de auditoria que não sabe **quem** acessou é um contador de portas abertas. A É8-27 só vale o custo depois da É8-13.

### Épico 4 — #54 · Rate limiting · **11 SP**

> **O que é:** a placa de **"não bata mais que 20 vezes"** na porta. Sem limite, uma requisição malformada em loop gera ping em todo equipamento monitorado, a cada 5 segundos, para sempre.

| ID | Task | Critério de aceite | SP |
|---|---|---|---|
| É8-19 | Decisão de camada e limites por classe de endpoint | Decisão registrada (D2: in-process) | 1 |
| É8-20 | Limiter com chave por IP/cliente; `/stats` e `/monitoramento` (os que disparam ping) com limite próprio | Limite excedido → **429** | 3 |
| É8-21 | Resposta 429 padronizada, com `Retry-After` | Corpo e header padronizados | 1 |
| É8-22 | Frontend: tratar 429 no polling (estado degradado, sem spam de erro no console) | Console limpo em regime normal | 2 |
| É8-23 | Testes: estourar o limite → 429; **o polling de 5s NUNCA toma 429** | 12 req/min do painel passam | 3 |
| É8-24 | Atualizar os RNFs de disponibilidade/segurança (§7) | PRD atualizado | 1 |

> **O número que decide o limite:** o dashboard faz polling a cada **5 segundos** = **12 requisições por minuto** por cliente. Qualquer limite abaixo de ~30/min **derruba o produto**. O AC da É8-23 existe para travar esse número.

### Épico 5 — #52 · TLS/HTTPS via reverse proxy (nginx) · **10 SP** · ⚠️ Onda 3, condicionada

> **O que é:** envolver a porta de metal. Hoje a comunicação entre o navegador e a API acontece em texto puro na rede — sem isso, quem estiver no mesmo fio lê o conteúdo.

| ID | Task | Critério de aceite | SP |
|---|---|---|---|
| É8-06 | Decisão de certificado (self-signed vs. Let's Encrypt) | Decisão registrada | 0 |
| É8-07 | Serviço nginx no compose + `proxy_pass` para `api:8000` e para o frontend | Compose sobe com 3 serviços | 3 |
| É8-08 | TLS: certificado, redirect 80→443, `HSTS`, `X-Content-Type-Options` | `https://` responde; headers presentes | 3 |
| É8-09 | `CORS_ORIGINS` → origem `https://`; URL da API do frontend → `https://` | Painel carrega **via https**, sem 403 no preflight | 2 |
| É8-10 | Rito de 8 passos reexecutado **por https** | 8/8 | 2 |

> **A ressalva do PO (D3):** este é o épico de **menor valor e maior risco** do lote. Sem cliente, sem domínio e sem operação contínua (§11.1), um certificado self-signed protege uma rede que não existe. E ele é o que mais pode quebrar a V1 — muda a origem do CORS, a URL da API e o preflight. **A recomendação é transferi-lo para a V2** (§8), onde já existem frontend de produção e operação real. Enquanto isso, ele é a última onda: se a V1 quebrar aqui, a Onda 3 é adiada e a #52 vai para a V2 sem perder nada.

---

## 4. Resumo e estimativa

| Épico | Issue | SP | Branch | Onda | Risco |
|---|---|---|---|---|---|
| 1 — Dados sensíveis | #51 | 6 | `feature/e8-51-mock-data` | 1 | 🟢 baixo |
| 2 — Autenticação real | #53 | 20 | `feature/e8-53-auth-real` | 1 | 🔴 alto |
| 3 — Logging + auditoria | #55 | 12 | `feature/e8-55-logging` | 2 | 🟡 médio |
| 4 — Rate limiting | #54 | 11 | `feature/e8-54-rate-limit` | 2 | 🟡 médio |
| 5 — TLS/HTTPS | #52 | 10 | `feature/e8-52-tls` | 3 | 🔴 alto |
| **TOTAL** | | **59** | **5 branches** | | |

**Capacidade de referência:** a sprint anterior entregou 42 SP em 6 dias (≈ 7 SP/dia, 1 dev). Nestas proporções: **Onda 1 = 4 dias · Onda 2 = 3,5 dias · Onda 3 = 1,5 dias**.

**Sem a Onda 3 (cenário recomendado, D3): 49 SP ≈ 7 dias úteis → 26/10 a 04/11, milestone fecha 06/11.**
**Com a Onda 3: 59 SP ≈ 8,5 dias úteis → fecha 06/11 do mesmo jeito.** A data de 06/11 cobre os dois cenários.

---

## 5. Ondas e ordem de execução

```
ONDA 1 — 26 SP (~4 dias) — 26/10 a 29/10
  Épico 1 (#51, 6 SP)   ┐ paralelos
  Épico 2 (#53, 20 SP)  ┘
  └─ Épico 1 não bloqueia nada: guardrail, fecha rápido e barato
  └─ Épico 2 é a peça central — NADA que dependa de identidade começa antes

ONDA 2 — 23 SP (~3,5 dias) — 30/10 a 04/11
  Épico 3 (#55, 12 SP)  ┐ paralelos
  Épico 4 (#54, 11 SP)  ┘
  └─ ambos aproveitam a identidade entregue na Onda 1

ONDA 3 — 10 SP (~1,5 dias) — 05/11 a 06/11  ⚠️ CONDICIONADA
  Épico 5 (#52, 10 SP)
  └─ decisão no fim da Onda 2: executa ou transfere para a V2 (§8)
```

**Regra de parallelismo (da sprint anterior):** no máximo **2 tasks em IN PROGRESS** ao mesmo tempo (o board tem limite de 2 no status). Épicos de ondas diferentes nunca correm juntos.

---

## 6. Dependências

```
#53 (auth real)  ──→  #55 (auditoria precisa saber QUEM acessou)
                 └──→  #54 (chave por usuário é melhor que só por IP — mas não obrigatória)

#52 (TLS)        ──→  #54 (SOMENTE se o limite for feito no nginx — D2 optou por in-process, então a seta não existe)

#51 (mock_data)  ──→  nada
```

**Por que a #52 ficou de fora do caminho da #54:** a D2 escolheu o limiter in-process justamente para manter isso assim. Se a D2 for revertida, a #54 passa a depender da #52 e a Onda 2 só pode começar depois da Onda 3 — o plano inteiro muda.

---

## 7. Fluxo Kanban

```
┌─────────────┐    ┌─────────┐    ┌──────────────┐    ┌──────────────────┐    ┌──────────────┐    ┌──────┐
│  BACKLOG    │───▶│  TO DO  │───▶│ IN PROGRESS  │───▶│ MERGE → develop  │───▶│ CODE REVIEW  │───▶│ DONE │
│  (nenhuma   │    │ (#51..  │    │  (máx. 2)    │    │ (feature merge)  │    │  (PO review) │    │      │
│  #51..#55)  │    │  #55)   │    │              │    │                  │    │              │    │      │
└─────────────┘    └─────────┘    └──────────────┘    └──────────────────┘    └──────────────┘    └──────┘
                                                                                                       │
                                                                                                       ▼
                                                                                               ┌──────────────┐
                                                                                               │ MERGE → main │
                                                                                               │ (final da    │
                                                                                               │  sprint)     │
                                                                                               └──────────────┘
```

**Regras (herdadas da sprint anterior):**
- No máximo **2 tasks** em IN PROGRESS ao mesmo tempo
- Feature só vai para MERGE → develop após **validação local** (compose + rito de 8 passos)
- Task só vai para DONE após **PO review no develop + rito reexecutado**
- Merge `develop` → `main` **uma única vez ao final da sprint** (a exceção para correção crítica está em `docs/sprint-v1-funcional-seguranca.md`)
- Bloqueios são sinalizados imediatamente

---

## 8. Definition of Ready (nova)

Toda issue precisa passar por estes 5 portões **antes** de entrar em TO DO:

- [ ] A **função está definida** e reescrita na issue (PRD §11.2) — sem "melhorar a segurança", com "quem faz o quê"
- [ ] Os **critérios de aceite são observáveis**, escritos em BDD, e incluem o rito de 8 passos
- [ ] A **dependência** com a #53 está resolvida ou declarada como "não"
- [ ] **Story point estimado** e branch nomeada (`feature/e8-<id>-<slug>`)
- [ ] **Modo de falha e de rollback** definidos (o que acontece se a feature for ligada e der errado em produção... ou seja, no rito)

---

## 9. Definition of Done

**Por task (DONE por task):**
- [ ] Código implementado e testado localmente
- [ ] `docker compose up` roda sem erros (na branch)
- [ ] **Rito de 8 passos reexecutado na branch** (§10) — não só teste automatizado
- [ ] **Modo opt-in testado nos dois estados**: feature ligada e desligada
- [ ] 0 respostas 401/403 novas no caminho do painel
- [ ] Nenhum `str(e)` exposto na API
- [ ] Nenhum segredo em log (verificado por teste)
- [ ] **PRD atualizado no mesmo PR** (§11.5)
- [ ] Issue atualizada com a evidência do rito
- [ ] PO fez review no `develop`
- [ ] Commit na branch da feature + merge da feature → `develop`

**Por épico (DONE por épico):**
- [ ] Todas as tasks do épico em DONE
- [ ] Rito de 8 passos reexecutado no `develop` (não só na branch)
- [ ] A referência do painel segue **R$ 803,85 / 5 concluídas / 3 falhas**
- [ ] Nenhuma issue do épico fica aberta sem decisão registrada
- [ ] **Milestone do épico fechado** (a regra de `docs/sprint-v1-funcional-seguranca.md`)

**Por sprint (DONE por sprint):**
- [ ] Todas as features mergeadas em `develop`
- [ ] `docker compose up` completo no `develop` sem erros
- [ ] Rito de 8 passos completo no `develop`
- [ ] PO validou o sistema integrado no `develop`
- [ ] Merge `develop` → `main` com **merge commit** + tag
- [ ] **Milestone É8 fechado**

---

## 10. Rito de aceitação (os 8 passos)

O rito da #67, que provou que 4 dos 8 passos falhavam na primeira rodada. **Toda task que muda comportamento observável o executa inteiro** — nos dois estados (opt-in ligado e desligado), quando houver.

| # | Passo | O que se olha |
|---|---|---|
| 1 | Sobe sem `backend/.env` e sem `env_file` | Só as variáveis explícitas |
| 2 | `GET /health` | 200 `{"status":"healthy","db_connected":true}` |
| 3 | `GET /stats` | 200, **R$ 803,85**, 5 concluídas, 3 falhas |
| 4 | `OPTIONS` com `Origin` | 200 + `access-control-allow-origin` |
| 5 | Dashboard na tela | Card de vendas, contagem de falhas, badge de erros |
| 6 | `GET /arquivos` | **15 arquivos, 0 ERRO** |
| 7 | Navegar nas 4 rotas | `/`, `/leituras`, `/cameras`, `/validacao` — sem erro no console |
| 8 | Polling de 5s | Requisições se sobrepõem? O console fica limpo? |

**Passos extras do É8:**
- 9 | Login: credencial errada → 401 genérico; correta → painel abre
- 10 | Rate limit: estourar o limite → 429 com `Retry-After`; **polling normal nunca toma 429**
- 11 | Log: toda requisição tem `request-id`; senha e token não aparecem em lugar nenhum
- 12 | `git ls-files mock_data` não lista nenhum arquivo sensível

---

## 11. KPIs do É8

| Métrica | Alvo | Como se mede |
|---|---|---|
| Segredos versionados | **0** | `git ls-files mock_data` + revisão da lista sensível |
| Linhas de log em JSON | **100%** | amostragem do container |
| Requisições com `request-id` | **100%** | amostragem |
| Segredos em log | **0** | teste automatizado de redação (É8-28) |
| 401/403 novos no caminho do painel | **0** | rito, passo 5 e 7 |
| Integridade do painel | **R$ 803,85 / 5 / 3** | rito, passo 3 |
| Issues do É8 com AC verificado | **5/5** | board em ✅ DONE |
| Épicos que fecharam sem rito | **0** | Definition of Done |

---

## 12. Riscos

| Risco | Por que é real | Mitigação |
|---|---|---|
| **Ligar a auth quebra o painel** | É literalmente a §11.4 | Modo opt-in (`AUTH_ENABLED`); rito nos **dois** estados; AC de integridade da referência |
| **O rate limit derruba o polling** | 12 req/min é o regime normal | Limite > 30/min; AC explícito: polling normal nunca toma 429 |
| **Remover mock quebra o "15 arquivos, 0 ERRO"** | O `mock_data` cobre 14 dos 15 (§11.4) | AC de não-regressão na É8-03; fixtures genéricas no lugar |
| **A auditoria loga senha ou token** | A auditoria passa pelo login | Teste automatizado de redação (É8-28) |
| **TLS quebra o preflight** | Muda a origem do CORS | Preflight já isento por método (#64); allowlist vira `https://`; rito inteiro por https |
| **É8 vira o novo "42 SP sem demonstração"** | §11.3 | Rito **por épico**; a V1 continua observável durante o É8 |
| **Escopo do #53 crescer** | Refresh token, 2FA, roles, OIDC — tudo cabe "num minutinho" | Escopo da Onda 1 **travado** nesta tabela; o que não está aqui vai para a V2 |
| **D2 ser revertida** | `limit_req` do nginx serializa as ondas | A onda 2 passa a depender da onda 3 → replanejar antes da Onda 2 |

---

## 13. Fora do escopo do É8

**Explicitamente não entra:**
- Matriz de roles `analista/supervisor/admin` → **V2** (§8)
- OIDC / SSO corporativo → **V2**
- Refresh token, 2FA, recuperação de senha → **V2**
- TLS com certificado real (Let's Encrypt) → **V2** (exige domínio)
- Rate limit distribuído / Redis → **V2**
- Trilha de auditoria **persistente em banco** → **V3** (§8, "Histórico persistente")
- SIEM, integração com Zabbix para logs → **V3**
- Reescrita de histórico do git → **nunca** (rota de rotação de segredo, não de reescrita)
- Monitor de expiração de certificado → **V2**

**E, antes que a lista de pendências do PRD seja confundida com o escopo do É8:** o §8 do PRD tem **7 itens de V2** (diagnóstico de VPAR, saúde do sistema, câmeras reais, leitoras reais, config dinâmica, WebSockets, auth+roles). **Nenhum deles é do É8.** O É8 é segurança e **não pode** competir com a entrega funcional — a §11.1 é explícita: *"endurecimento não pode consumir a entrega da funcionalidade"*. A V2 e o É8 disputam o mesmo tempo do time; o PO precisa escolher a ordem. **Recomendação do PO: É8 primeiro, porque é o que está escrito no milestone — e a V2 é grande demais para entrar junto.**

---

## 14. Pendências que este plano não resolve

| Pendência | Onde fica |
|---|---|
| O frontend não envia `X-API-Key` (§6.7) | Continua assim até a É8-15 — e passa a ser token, não API Key |
| Isolamento de filesystem `:ro` (§7) | Fora do escopo da V1 (o mount precisa ser gravável para o `entrypoint.sh`) |
| `python-multipart` e `httpx` no `requirements.txt` sem uso evidente | Não é do É8 — dívida de higiene, para a V2 |
| Câmeras e Leitoras mockadas (FR-14/16) | V2 |
| Testes de frontend (component tests) | V3 (§8) |

---

*Documento vivo — o PO atualiza o status das tasks aqui a cada revisão de sprint.*
*Regra: toda alteração de comportamento observável atualiza o PRD no mesmo PR (§11.5 do PRD).*
