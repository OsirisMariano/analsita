# Sprint É8 — Segurança & Evolução

> **Status:** Planejado pelo PO em 21/10/2026. **Reescopado em 21/10/2026** para a capacidade real de 2 h/dia.
> **Milestone:** [É8 — Segurança & Evolução](https://github.com/OsirisMariano/analsita/milestone/8) · **Janela:** 26/10/2026 → **04/12/2026** · **Checkpoint:** 13/11/2026
> **Escopo:** **40 SP** em 4 ciclos · **Base:** PRD v1.7 §5.2, §7, §8, §11.1–11.5, §12 · código em `develop` (`9ac2f18`)
> **Issues:** [#51](https://github.com/OsirisMariano/analsita/issues/51) · [#53](https://github.com/OsirisMariano/analsita/issues/53) · [#55](https://github.com/OsirisMariano/analsita/issues/55)

---

## 1. O problema que vamos resolver

**Em uma frase:** o painel de hoje mostra *o que* está quebrado no posto, mas não mostra *quem* olhou — então a validação de um equipamento é um número sem assinatura.

**A analogia:** o galpão do posto tem mercadoria na prateleira, e já existe um livro de ponto — mas é um livro de ponto **anônimo**. Qualquer um que entre anota "tudo certo". Quando o equipamento trava às 3h da manhã, ninguém sabe se o técnico passou, o que ele viu, nem se alguém sequer olhou. O É8 não constrói mais prateleira: ele **assina o livro**. Quem entra diz quem é, e o que ele faz fica registrado.

**O que isso tem a ver com o field service:** o técnico de campo tem uma janela curta para validar os equipamentos do posto. O É8 não dá velocidade a ele — **dá rastreabilidade**. Quem valida, quando, e com que resultado. A *velocidade* (reinício real de leitora, diagnóstico de VPAR, câmeras reais) é a **V2** (PRD §8). O É8 entrega a camada de **confiança** sobre a qual a velocidade vai se apoiar.

**Por que agora, e não antes:** o PRD §11.2 classificava essas pendências como *"backlog sem prazo — reescritos quando as funções estiverem definidas"*. A função da V1 agora **está** definida e observada no browser (a #67 provou em 21/10). Endurecer a porta antes de o painel ser confiável é erguer parede em casa sem chão.

**Por que agora, e não depois:** o §11.3 registra o preço de errar a ordem — 42 SP de hardening enquanto a V1 nunca foi demonstrada funcionando. O É8 inverte a ordem: **cada ciclo fecha com o painel verificado e com algo para mostrar**.

---

## 2. Decisões do PO (D1–D8)

As 5 issues do É8 foram escritas como pendências soltas em 01/10/2026. Para planejar, elas precisavam de decisões que não cabem no texto de uma issue. **D1–D5** fecharam o plano; **D6–D8** vieram da resposta de capacidade.

| # | Decisão | Escolha | Por quê | Custo se fosse diferente |
|---|---|---|---|---|
| **D1** | Onde fica a identidade dos usuários? | **`auth.db` separado** (SQLite gravável), criado pelo `entrypoint.sh` | A API abre o banco de transactions com `mode=ro` (§7) — ela **não pode gravar** uma tabela de usuários no mesmo arquivo | OIDC exigiria um provedor de identidade externo; a §11.1 diz que não há operação contínua nem rede de produção. Seriam ~10 SP a mais e uma dependência que o projeto de estudos não tem |
| **D2** | Onde fica o rate limit? | **In-process**, no FastAPI (chave por IP/cliente) | Mantém a #54 **independente** da #52 e permite as ondas em paralelo | `limit_req` do nginx custaria +1 SP, mas serializaria as ondas 2 e 3 |
| **D3** | A #52 (TLS) executa no É8? | ❌ **NÃO. Transferida para a V2** (milestone "V2 — Operacional") | Certificado self-signed, sem domínio, sem cliente e sem operação contínua (§11.1) é **teatro com o custo mais alto do lote**. E é a issue que mais pode quebrar a V1: muda a origem do CORS, a URL da API e o preflight | TLS real (Let's Encrypt) exige domínio — fora do alcance de um projeto de estudos |
| **D4** | O escopo de papéis (roles) entra? | **Não.** O É8 entrega **identidade + 1 nível** (`admin` / leitura) | A matriz `analista/supervisor/admin` é item da **V2** (§8). E papel sem tela para usá-lo é código morto | 3 SP de matriz de papéis, sem valor observável |
| **D5** | Quando o É8 fecha? | **04/12/2026**, começando em 26/10/2026 — com **checkpoint em 13/11/2026** | Ver D6: a data é uma **previsão** que o checkpoint recalibra com taxa medida | — |
| **D6** | Qual é a capacidade real? | **2 h/dia** (1 sessão curta por dia) → **~1,5 SP por sessão** | A "referência de 7 SP/dia" da sprint anterior era a *previsão* de uma sessão de dia inteiro, não uma medição. Ver §4 | Com 7 SP/dia, 40 SP sairiam em 6 dias — data que o histórico do projeto já provou falsa |
| **D7** | A #54 (rate limit) fica no É8? | ❌ **NÃO. Transferida para o É9** (milestone "É9 — Hardening follow-up") | 11 SP — **20% do orçamento** — para o item de menor valor visível do lote. A 2 h/dia o tempo é o recurso mais escasso, e o portfólio ganha 10x mais com "a validação saiu assinada" do que com "a API devolve 429" | 49 SP e o fechamento em janeiro |
| **D8** | A trilha de auditoria é visível? | ✅ **SIM — +2 SP (É8-27b)**: `GET /auditoria` (ring buffer em memória) + card na view de validação | Um portfólio sobre "agilidade no field service" que só mostra tela de login **promete demais**. Com a trilha no painel, a demo conta a história inteira: o técnico entra, o painel valida, o registro sai assinado | A história fica no log do servidor, invisível para quem abre o repo |

> **D3 e D7 são o mesmo movimento, e ele tem um nome:** *capar o É8, não justificá-lo*. O §11.1 é explícito — *"endurecimento não pode consumir a entrega da funcionalidade"*. Com 2 h/dia, "consumir" é literal.
>
> **Nenhuma issue fica órfã:** a #52 ganhou o milestone "V2 — Operacional" e a #54 ganhou o milestone "É9 — Hardening follow-up". O problema que a hygiene de board resolveu mais cedo nesta noite (issue sem milestone) não volta.

---

## 3. O que será construído (3 épicos, 40 SP)

**Plano (sem jargon, para quem nunca leu o código):** cada épico abaixo tem uma frase que explica o resultado, a lista de tasks com o critério de aceite, e os story points. O critério de aceite de toda task que muda comportamento observável passa pelo **rito de 8 passos** da §10.

### Épico 1 — #51 · Dados sensíveis fora do versionamento · **6 SP** · Ciclo 1

> **O que é:** garantir que o repositório nunca guarde credencial de posto de verdade. Hoje ele não guarda nenhuma — os 19 arquivos de `mock_data/` são placeholders ("mock license data", `Server=192.0.2.1`). O trabalho real é **erguer a cerca antes que alguém traga a senha da loja**.

| ID | Task | Critério de aceite | SP |
|---|---|---|---|
| É8-01 | Auditar os 19 arquivos de `mock_data/` e **declarar** a lista de sensíveis por definição (licença, certificado, `posto.json`, `concentrador.json`) | Relatório versionado: 19 arquivos, 0 segredo real, 3 IPs de LAN em 7 mocks | 1 |
| É8-02 | Remover do git os sensíveis (`git rm --cached`) e declará-los no `.gitignore` | `git ls-files mock_data` não lista nenhum arquivo da lista sensível | 1 |
| É8-03 | Substituir por fixtures **genéricas** que preservem a validação | `GET /arquivos` continua retornando **15 arquivos, 0 ERRO** — e o **clone limpo** também | 2 |
| É8-04 | Escrever a regra "nunca versionar" no `.gitignore` comentado + neste doc | Regra versionada, legível, com a orientação de **rotacionar** (não reescrever histórico) se um segredo real entrar | 1 |
| É8-05 | Atualizar o PRD no mesmo PR (§11.5) | PRD atualizado | 1 |

> **É8-01 está FEITA** — o relatório está em [§3.1](#31-relatório-da-auditoria-é8-01-concluída-em-21102026). O que resta no ciclo 1 é a É8-02 e a É8-03, **que têm que entrar no mesmo PR**: `mock_data/` alimenta os arquivos que o painel valida via **7 mounts** do compose, e um `git rm --cached` sem fixture genérica no mesmo caminho quebra o "15 arquivos, 0 ERRO" no clone limpo.

#### 3.1 Relatório da auditoria (É8-01, concluída em 21/10/2026)

| Métrica | Resultado |
|---|---|
| Arquivos versionados em `mock_data/` | **19** |
| Segredos reais encontrados | **0** |
| Dados não-placeholder | **3 IPs de LAN** (`192.168.1.10`, `192.168.1.11`, `192.168.212.21`) em **7 arquivos** |
| Dados de documentação (RFC 5737) | `192.0.2.1` em `zabbix_agent2.conf` — faixa reservada para documentação |
| Arquivos "sensíveis por definição" (8) | `licenca.V2C` (18 B), `cert.p12` (17 B), `posto.json` ×2, `postoAberto.json` ×2, `concentrador.json` ×2 |

**Onde estão os 3 IPs de LAN:**

| IP | Arquivos |
|---|---|
| `192.168.212.21` | `lado1/antena.json`, `lado1/camera.json` (3 campos), `lado2/antena.json`, `lado2/camera.json` (3 campos), `autorizador/retrofit-autorizador.json` |
| `192.168.1.10` | `lado1/concentrador.json` |
| `192.168.1.11` | `lado2/concentrador.json` |

**Conclusões que viram regra:**

1. **O #51 é guardrail de futuro, não limpeza de hoje.** O risco real é alguém comitar um `posto.json` de verdade no próximo serviço.
2. **O histórico do git não precisa ser reescrito.** Não há segredo real nele, e reescrever invalidaria as tags `v1.0.0`/`v1.0.1` sem comprar segurança nenhuma. **Se um dia entrar um segredo real, a providência é rotacionar o segredo — nunca reescrever o histórico.**
3. **Os 3 IPs de LAN saem da lista de sensíveis**, porque `192.168.x.x` é faixa privada e o valor é de mock. Ficam na lista por serem dados de infraestrutura *de posto*, mas a regra que vale é a do item 1: o que for de um posto real não entra.

### Épico 2 — #53 · Autenticação real (login/senha) · **20 SP** · Ciclo 2

> **O que é:** trocar a corrente no portão por uma **porta com fechadura**. Quem abre precisa de usuário e senha; a API passa a saber **quem** é a pessoa, não só se a requisição tem um carimbo.

| ID | Task | Critério de aceite | SP |
|---|---|---|---|
| É8-11 | Decisão de identidade: store, algoritmo de hash, formato e validade do token | ADR curto neste doc | 1 |
| É8-12 | Criar `auth.db` **separado** (a API é `mode=ro` no banco de transactions) com tabela `usuarios` + seed | Schema criado pelo `entrypoint.sh`; 1 usuário admin; senha **só** com hash | 3 |
| É8-13 | `POST /auth/login` — verifica hash, emite token de curta duração | Credencial correta → token; senha errada → **401** genérico | 3 |
| É8-14 | Middleware de autenticação + rotas isentas (`/health`, `/docs`, `/openapi.json`, `/redoc`, login) + **`OPTIONS` isento por método** | O preflight responde **200** — não repetir o bug do §11.4 | 3 |
| É8-15 | Frontend: tela de login + injeção do token em `api.js` (fonte única da URL) | `api.js` passa a enviar a credencial; painel abre após o login | 3 |
| É8-16 | **Modo opt-in por env** (`AUTH_ENABLED`), espelhando o padrão da #63 | Sem `AUTH_ENABLED`, a API se comporta exatamente como hoje | 3 |
| É8-17 | Testes: login ok · senha errada · token expirado · rota isenta · preflight · modo off | Os 6 cenários cobertos | 3 |
| É8-18 | Atualizar FR-19 no PRD + §10 | PRD no mesmo PR (§11.5) | 1 |

> **O porquê do modo opt-in:** é o **mesmo padrão que a #63 já provou** para a API Key (opt-in, `API_KEY` ausente = sem credencial). O motivo não é segurança — é **não repetir a §11.4**: se a autenticação virar obrigatória e o frontend não souber falar com ela, o painel inteiro quebra. O opt-in permite rodar o rito **nos dois modos**: com e sem autenticação.
>
> **O ADR da É8-11 tem 3 decisões que o plano deixou para a implementação** (e o PO já tem preferência, para não gastar tempo: store = `auth.db` no volume gravável `/var/abastece/dados/`; hash = `hashlib.pbkdf2_hmac` da stdlib, **zero dependência nova**; token = **opaco guardado no `auth.db`**, não JWT — revogável, sem chave de assinatura para gerenciar, e cabe nos 3 SP da É8-13).

### Épico 3 — #55 · Logging estruturado e auditoria · **14 SP** · Ciclos 3 e 4

> **O que é:** trocar o papelote ("deu erro") por um **livro de ponto assinado**. Cada requisição vira uma linha estruturada com nível, `request-id`, tempo de resposta e, nos endpoints sensíveis, **quem** acessou. E — o que faz a diferença no portfólio — **esse livro aparece no painel**.

| ID | Task | Critério de aceite | SP | Ciclo |
|---|---|---|---|---|
| É8-25 | Logging estruturado em JSON (formatter próprio sobre `logging` da stdlib — **zero dependência nova**) | 100% das linhas em JSON, com `level` | 3 | 3 |
| É8-26 | Middleware de `request-id` (gera ou propaga `X-Request-ID`) | 100% das requisições com id no log | 2 | 3 |
| É8-29 | Trocar os 4 `print()` de `backend/app/` por logging com nível | 0 `print()` em `backend/app/` | 1 | 3 |
| É8-30 | Atualizar o RNF de Observabilidade (§7) | PRD atualizado | 1 | 3 |
| É8-27 | Trilha de auditoria nos endpoints sensíveis (`/auth/login`, `/stats`, `/monitoramento`, `/arquivos`), **com usuário quando houver** | Entrada com `usuario`, `ip`, `status`, `duracao_ms` | 3 | 4 |
| É8-28 | **Redação de segredos**: senha e token nunca no log | Teste automatizado que **falha** se vazar | 2 | 4 |
| **É8-27b** | **Trilha visível no painel**: `GET /auditoria` (ring buffer em memória, **sem persistência**) + card na view de validação | O painel mostra a última validação com **quem** validou, **quando** e **quantos arquivos OK** | **2** | 4 |

> **Por que a auditoria vem depois da #53:** uma trilha de auditoria que não sabe **quem** acessou é um contador de portas abertas. A É8-27 só vale o custo depois da É8-13.
>
> **Por que a É8-27b existe (D8):** sem ela, a história do field service fica no log do servidor — invisível para quem abre o repo. Com ela, a demo é: **técnico entra → painel valida os 15 arquivos → o registro aparece assinado na tela.** É o único artefato do É8 que serve aos dois públicos ao mesmo tempo.

### Épicos transferidos (fora do É8)

| Épico | Issue | SP | Destino | Decisão |
|---|---|---|---|---|
| TLS/HTTPS via nginx | [#52](https://github.com/OsirisMariano/analsita/issues/52) | 10 | Milestone **"V2 — Operacional"** | **D3** |
| Rate limiting | [#54](https://github.com/OsirisMariano/analsita/issues/54) | 11 | Milestone **"É9 — Hardening follow-up"** | **D7** |

---

## 4. Capacidade, estimativa e os 4 ciclos

### 4.1 A taxa real (correção de uma estimativa que virou fato)

O primeiro plano deste sprint apoiou-se em **"a sprint anterior entregou 42 SP em 6 dias (≈ 7 SP/dia)"**. **Isso é a estimativa do doc, não o fato.** O que o histórico mostra:

| | |
|---|---|
| O doc da sprint anterior diz | "Duração **estimada**: 6 dias úteis" |
| O que aconteceu | 24/08 (seg) → 10/09 (qui) = **14 dias úteis de calendário** |
| E o diário registra | 24/08, 25/08, **05/09 (sábado)**, 09/09, 10/09 — com um **buraco de 9 dias corridos** (26/08 → 04/09) sem nenhuma entrada |
| Entregue | **36 dos 42 SP** (o É6 foi cancelado) |
| **Unidade real de ritmo** | **SP por sessão de trabalho**, não SP por dia de calendário |

A sprint anterior entregou 36 SP em **~5 sessões concentradas** espalhadas por 3 semanas. A "referência de 7 SP/dia" era a previsão de uma sessão de **dia inteiro**.

**A capacidade deste sprint é 2 h/dia = 1 sessão curta por dia.** Três cenários, e o **ciclo 1 é a medição**:

| Cenário | Taxa | 40 SP | É8 fecha |
|---|---|---|---|
| Otimista (2,5 SP/sessão) | sessão curta rende quase dia inteiro | 16 dias úteis | ~18/11/2026 |
| **Central (1,5 SP/sessão)** | 2 h com overhead de contexto | 27 dias úteis | ~**04/12/2026** ← **D5** |
| Pessimista (0,7 SP/sessão) | o overhead domina | 57 dias úteis | ~15/01/2027 |

> **O `due_on` de 04/12 é uma previsão, não uma promessa.** O **checkpoint de 13/11/2026** (depois do ciclo 1, com taxa medida) recalibra a data e o escopo restante. É o acordo: previsão com ponto de reavaliação.

### 4.2 Os 4 ciclos

| Ciclo | Épicos | SP | Janela (cenário central) | Artefato que fecha o ciclo | Milestone |
|---|---|---|---|---|---|
| **1** | #51 | 6 | 26/10 → 29/10 | "o repo não guarda segredo" + **a taxa real medida** | É8 |
| **2** | #53 | 20 | 30/10 → 17/11 | **tela de login** — "cada técnico tem seu acesso" | É8 |
| **3** | #55a (É8-25, 26, 29, 30) | 7 | 18/11 → 24/11 | log JSON + `request-id` | É8 |
| **4** | #55b (É8-27, 28) + É8-27b | 7 | 25/11 → 04/12 | 🎯 **a trilha de auditoria no painel** — "a validação saiu assinada" | É8 |
| | **TOTAL** | **40** | | | |

**A ordem é pela demo, não só pela dependência.** O ciclo 3 (log JSON) é o que torna a É8-27 bem feita, e o ciclo 4 é o que fecha a história. O ciclo 1 vem primeiro porque é o mais barato, não tem risco de runtime e **é a medição da taxa**.

### 4.3 Regra de paralelismo

O board permite **2 tasks** em IN PROGRESS, mas o time é **1 pessoa**. A tradução honesta: **1 slot de código + 1 slot de decisão/documento**. Duas branches com teclado ao mesmo tempo é imposto de contexto, não paralelismo.

---

## 5. Dependências

```
#53 (auth real)  ──→  #55b (É8-27: auditoria precisa saber QUEM acessou)
                 └──→  É8-27b (a trilha só mostra "quem" se existir identidade)

#55a (É8-25, 26, 29, 30)  ──→  nenhuma! (9 SP de logging JSON, request-id,
                                       redação de base e PRD não dependem da #53)

#51 (mock_data)  ──→  nada
```

> **Correção do primeiro plano:** a versão anterior amarrou o épico de logging inteiro à #53. O gráfico de dependência justificava só **3 dos 12 SP**. Desamarrar compra folga de cronograma sem cortar escopo — e permite rodar o ciclo 3 **em paralelo** com o fim do ciclo 2.

---

## 6. Fluxo Kanban

```
┌─────────────┐    ┌─────────┐    ┌──────────────┐    ┌──────────────────┐    ┌──────────────┐    ┌──────┐
│  BACKLOG    │───▶│  TO DO  │───▶│ IN PROGRESS  │───▶│ MERGE → develop  │───▶│ CODE REVIEW  │───▶│ DONE │
│  (#52, #54) │    │ (#51,   │    │  (2 slots:   │───▶│ (feature merge)  │    │  (PO review) │    │      │
│             │    │  #53,   │    │  1 código +  │    │                  │    │              │    │      │
│             │    │  #55)   │    │  1 decisão)  │    │                  │    │              │    │      │
└─────────────┘    └─────────┘    └──────────────┘    └──────────────────┘    └──────────────┘    └──────┘
                                                                                                       │
                                                                                                       ▼
                                                                                               ┌──────────────┐
                                                                                               │ MERGE → main │
                                                                                               │ (final do    │
                                                                                               │  É8)         │
                                                                                               └──────────────┘
```

**Regras (herdadas da sprint anterior):**
- No máximo **2 tasks** em IN PROGRESS — **1 de código + 1 de decisão/documento**
- Feature só vai para MERGE → develop após **validação local** (compose + rito de 8 passos)
- Task só vai para DONE após **PO review no develop + rito reexecutado**
- Merge `develop` → `main` **uma única vez ao final do É8** (a exceção para correção crítica está em `docs/sprint-v1-funcional-seguranca.md`)
- Bloqueios são sinalizados imediatamente

---

## 7. Definition of Ready (nova)

Toda issue precisa passar por estes 5 portões **antes** de entrar em TO DO:

- [ ] A **função está definida** e reescrita na issue (PRD §11.2) — sem "melhorar a segurança", com "quem faz o quê"
- [ ] Os **critérios de aceite são observáveis**, escritos em BDD, e incluem o rito de 8 passos
- [ ] A **dependência** com a #53 está resolvida ou declarada como "não"
- [ ] **Story point estimado** e branch nomeada (`feature/e8-<id>-<slug>`)
- [ ] **Modo de falha e de rollback** definidos (o que acontece se a feature for ligada e der errado no rito)

---

## 8. Definition of Done

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

**Por ciclo (DONE por ciclo):**
- [ ] Todas as tasks do ciclo em DONE
- [ ] Rito de 8 passos reexecutado no `develop` (não só na branch)
- [ ] A referência do painel segue **R$ 803,85 / 5 concluídas / 3 falhas** (do banco semeado no dia — ver §10)
- [ ] **O artefato do ciclo está demonstrável** (ver §9, critério de demo)
- [ ] Nenhuma issue do ciclo fica aberta sem decisão registrada
- [ ] **Milestone do épico fechado**

**Por sprint (DONE por sprint):**
- [ ] Todos os 4 ciclos fechados
- [ ] `docker compose up` completo no `develop` sem erros
- [ ] Rito de 8 passos completo no `develop`
- [ ] **Demo registrada** (ver §9)
- [ ] PO validou o sistema integrado no `develop`
- [ ] Merge `develop` → `main` com **merge commit** + tag
- [ ] **Milestone É8 fechado**

---

## 9. Critério de qualidade externo (a demo)

> **Por que isto existe:** a §11.3 registra que hardening sem verificação produz entregas que não rodam. O risco equivalente do É8 é o oposto: **fechar 40 tasks no prazo e não provar nada**. O plano mede *quantas tasks fecharam*, não *o que foi provado*. Por isso o É8 fecha com uma **demonstração registrada**.

**A demo do É8 (registrada em print, vídeo ou transcrição no diário):**

| # | O que se mostra | Por que está nesta lista |
|---|---|---|
| 1 | **A tela de login** | "cada técnico tem seu acesso" — o artefato mais visível do É8 |
| 2 | **O técnico logado validando os 15 arquivos** | O painel continua funcionando: o É8 não quebrou a V1 |
| 3 | **A trilha de auditoria na tela** (É8-27b) | "a validação saiu assinada: quem, quando, o quê" — **a história do field service** |
| 4 | **O log JSON no terminal** com `request-id` | A mesma história, vista pelo operador |
| 5 | **O `GET /auditoria` respondendo** | A API expõe o registro, não só o terminal |

**Sem os 5, o É8 não fecha** — mesmo que as 40 tasks estejam em DONE. É o critério que o §11.3 pede, aplicado a um sprint de portfólio.

---

## 10. Rito de aceitação (os 8 passos + 4 do É8)

O rito da #67, que provou que 4 dos 8 passos falhavam na primeira rodada. **Toda task que muda comportamento observável o executa inteiro** — nos dois estados (opt-in ligado e desligado), quando houver.

> ⚠️ **Antes de cada sessão de rito: regerar o banco de referência.**
> O `/stats` filtra por `date(timestamp) = date('now','localtime')` (correção do #81) e as transações "de hoje" são carimbadas **no momento da simulação**. Um banco gerado ontem devolve **R$ 0,00** hoje. Sem este passo, o rito falha por um motivo que não tem nada a ver com o código em revisão — e a reação natural da equipe é "o AC está desatualizado".
>
> ```bash
> SIMULADOR_SEED=154622 python scripts/simulador_posto.py
> ```
>
> **A invariante é o procedimento, não o número literal:** *"as transações de hoje do banco semeado: 5 `CONCLUIDO` somando **R$ 803,85**, 2 `EM_ABERTO`, 3 `FALHA`"*. O **valor** é fixo pela semente; a **data** é a de hoje.

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
- 10 | Log: toda requisição tem `request-id`; senha e token não aparecem em lugar nenhum
- 11 | Auditoria: `GET /auditoria` devolve a última validação com `usuario`, `ip`, `status`, `duracao_ms`
- 12 | `git ls-files mock_data` não lista nenhum arquivo da lista sensível |

---

## 11. KPIs do É8

| Métrica | Alvo | Como se mede |
|---|---|---|
| Segredos versionados | **0** | `git ls-files mock_data` + revisão da lista sensível |
| Linhas de log em JSON | **100%** | amostragem do container |
| Requisições com `request-id` | **100%** | amostragem |
| Segredos em log | **0** | teste automatizado de redação (É8-28) |
| 401/403 novos no caminho do painel | **0** | rito, passos 5 e 7 |
| Integridade do painel | **R$ 803,85 / 5 / 3** (banco semeado no dia) | rito, passo 3 |
| **Demo do É8 registrada** | **1, com os 5 itens** | §9 |
| Issues do É8 com AC verificado | **3/3** | board em ✅ DONE |
| Épicos que fecharam sem rito | **0** | Definition of Done |

---

## 12. Riscos

| Risco | Por que é real | Mitigação |
|---|---|---|
| **Ligar a auth quebra o painel** | É literalmente a §11.4 | Modo opt-in (`AUTH_ENABLED`); rito nos **dois** estados; AC de integridade da referência |
| **O ciclo 1 vira medição e não entrega** | A É8-01 já está feita; a É8-02/03 muda o layout de arquivos do repo | É8-02 e É8-03 no **mesmo PR**, com AC de clone limpo |
| **A trilha de auditoria loga senha ou token** | A auditoria passa pelo login | Teste automatizado de redação (É8-28) |
| **A taxa real vier abaixo de 1,5 SP/sessão** | A referência é medida em outra margem de commitment | **Checkpoint em 13/11** recalibra data e escopo; o corte, se houver, é sempre na **Onda/Ciclo 2**, nunca no ciclo 1 |
| **2 h/dia se transforma em 1 sprint de 3 meses** | 40 SP ÷ 0,7 = 57 dias úteis | A data é previsão com checkpoint; e o **critério de demo** (§9) permite ter o artefato de portfólio antes do sprint fechar |
| **É8 vira o novo "42 SP sem demonstração"** | §11.3 | Rito **por ciclo**; demo **por sprint**; a V1 continua observável durante o É8 |
| **Escopo do #53 crescer** | Refresh token, 2FA, roles, OIDC — tudo cabe "num minutinho" | Escopo travado nesta tabela; o que não está aqui vai para a V2 |

---

## 13. Fora do escopo do É8

**Explicitamente não entra:**
- Matriz de roles `analista/supervisor/admin` → **V2** (§8) · OIDC/SSO → V2 · refresh token · 2FA · recuperação de senha → V2
- **TLS/HTTPS (#52)** → milestone **"V2 — Operacional"** (D3)
- **Rate limiting (#54)** → milestone **"É9 — Hardening follow-up"** (D7)
- Rate limit distribuído / Redis → V2 · limites configuráveis por ambiente → V2
- Trilha de auditoria **persistente em banco** → **V3** (§8, "Histórico persistente") — no É8 ela vive em **ring buffer de memória** (É8-27b)
- SIEM, integração com Zabbix para logs → V3 · métricas agregadas (Prometheus) → V3
- Reescrita de histórico do git → **nunca** (rota de rotação de segredo, não de reescrita)
- Monitor de expiração de certificado → V2

**E, antes que a §8 seja confundida com o escopo do É8:** os **7 itens da V2** (diagnóstico de VPAR, saúde do sistema, câmeras reais, leitoras reais, config dinâmica, WebSockets, auth+roles) **não são do É8**. A §11.1 é explícita: *"endurecimento não pode consumir a entrega da funcionalidade"*. Com 2 h/dia, essa disputa é literal: **o É8 são ~3 meses de noites, e a V2 é o que move a métrica de sucesso do §4.2** (reduzir MTTR). A recomendação do PO segue: **É8 primeiro** (é o milestone planejado, e a §9 define o critério de qualidade que um portfólio precisa), **V2 depois** — mas a decisão de ordem é do dono do projeto, e ela precisa ser tomada com a §4.2 aberta na mesa.

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

*Documento vivo — o PO atualiza o status das tasks aqui a cada ciclo.*
*Regra: toda alteração de comportamento observável atualiza o PRD no mesmo PR (§11.5 do PRD).*
