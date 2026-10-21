# Sprint V1 Funcional — Segurança

**Data:** 18/08/2026
**Objetivo:** Corrigir brechas de segurança identificadas na auditoria da Sprint V1 Funcional
**Gestão:** [GitHub Projects — Analista SemParar: Segurança & Evolução](https://github.com/users/OsirisMariano/projects/70) (Kanban com SEC-01..SEC-32, épicos e backlog futuro)

---

## O problema que resolvemos

A Sprint V1 Funcional entregou um sistema funcional com dados reais via API. Porém, uma auditoria de segurança identificou **19 vulnerabilidades** (3 Críticas, 5 Altas, 7 Médias, 4 Baixas). Esta sprint ataca as mais severas em 6 entregas incrementais.

---

## O que foi construído (6 entregas)

### 1. CORS + Autenticação (API Key)

**O que era:** A aceita CORS estava com `allow_origins=["*"]` + `allow_credentials=True`. Qualquer site da internet podia fazer requisições à API como se fosse um usuário autenticado. Não havia nenhuma autenticação em nenhum endpoint — qualquer pessoa lia transações e configurações.

**O que foi feito:**
- CORS restrito a origens específicas (ex: `http://localhost:5173`, `http://localhost:3000`)
- Métodos HTTP restritos a `GET` (todos os endpoints são read-only)
- Middleware de API Key (`X-API-Key`) em todos os endpoints
- Variável de ambiente `API_KEY` no backend

**Analogia:** Antes, a porta da casa estava aberta com um letreiro "pode entrar qualquer um". Agora, tem fechadura e só quem tem chave pode entrar.

**Vulnerabilidades resolvidas:** C-1, H-3

---

### 2. Validação de Input

**O que era:** A função `disparar_ping()` aceitava qualquer string como IP sem validação. Se alguém passasse um comando malicioso como IP (ex: `; rm -rf /`), ele seria executado via `subprocess.run`. Além disso, a função `extrair_valor()` em `validador.py` lia qualquer path do filesystem sem restrição.

**O que foi feito:**
- Validação de formato de IP com `ipaddress.ip_address()` antes do subprocess
- Whitelist de prefixos de path permitidos em `extrair_valor()` (ex: `/etc/abastece/`, `/var/abastece/`)
- Paths fora da whitelist retornam erro genérico

**Analogia:** Antes, o porteiro aceitava qualquer documento — até um papel escrito à mão. Agora, ele verifica se o documento é válido e se o visitante está na lista de convidados.

**Vulnerabilidades resolvidas:** C-2, M-5

---

### 3. Docker Hardening

**O que era:** Ambos os containers (backend e frontend) rodavam como `root`. Os mounts de `./scripts` e `./backend/app` eram graváveis — um atacante com acesso ao container podia modificar código em runtime. Não existia `.dockerignore`, então `COPY . .` copiava tudo (`.env`, `.git`, `__pycache__`). O `uvicorn --reload` rodava em produção.

**O que foi feito:**
- Criado usuário não-root (`appuser`) em ambos os Dockerfiles
- Todos os mounts marcados como `:ro` (read-only) exceto `/data` (necessário para escrita do SQLite)
- Criado `.dockerignore` no backend e na raiz do projeto
- Removido `--reload` do uvicorn no `entrypoint.sh`
- Adicionado `cap_add: [NET_RAW]` no docker-compose para o ping funcionar com usuário não-root

**Analogia:** Antes, o segurança trabalhava de pijama e deixava a porta da despensa destrancada. Agora, ele usa farda, a despensa trancada e só leva pra dentro o que é necessário.

**Vulnerabilidades resolvidas:** C-3, H-1, H-4, M-3, M-4

---

### 4. Error Handling

**O que era:** Exceções Python eram retornadas diretamente na resposta da API (`str(e)`). Erros de banco de dados revelavam caminhos do filesystem, nomes de colunas e detalhes do SQLite. Erros de leitura de arquivos em `validador.py` expunham exceções de I/O.

**O que foi feito:**
- Substituídas todas as respostas `detail=f"Erro: {str(e)}"` por mensagens genéricas
- Exceções logadas no servidor (`print()` ou `logging`) em vez de retornadas ao cliente
- Exemplo: `"Erro interno ao acessar o banco de dados"` em vez do traceback completo

**Analogia:** Antes, quando o carro quebrava, o mecânico gritava o problema alto pra rua inteira ouvir. Agora, ele anota no caderno e diz ao cliente "vamos resolver".

**Vulnerabilidades resolvidas:** H-2, M-7

---

### 5. Configuração + Segredos

**O que era:** IPs internos (`192.168.212.21`, `192.168.1.10`), código do conveniado (`02896`), nome do servidor SFTP (`DS_ABAST.02896_1`) e IP do Zabbix (`192.168.1.100`) estavam todos hardcoded no código-fonte e commitados no repositório. Qualquer pessoa com acesso ao repo sabia a topologia completa da rede.

**O que foi feito:**
- Todos os valores sensíveis movidos para variáveis de ambiente (`.env` do backend)
- Criado `.env.example` com placeholders (sem valores reais) para referência
- IP do Zabbix no mock substituído por endereço RFC 5737 (`192.0.2.1` — non-routable)
- Equipment IPs externizados para `EQUIPAMENTOS` via variável de ambiente

**Analogia:** Antes, o endereço da casa, a senha do cofre e o esquema de segurança estavam colados na porta da rua. Agora, estão dentro de um envelope lacrado que só o gerente abre.

**Vulnerabilidades resolvidas:** M-1, M-2, H-5, L-3

---

### 6. Frontend Produção

**O que era:** O container do frontend rodava `vite dev` (servidor de desenvolvimento) com `--host`. O Vite dev expõe HMR WebSocket (execução de código arbitrário), error overlays com snippets de código, e roda significativamente mais lento. O `--host` bindava em `0.0.0.0`, acessível de qualquer máquina na rede.

**O que foi feito:**
- Dockerfile alterado para build de produção (`npm run build`)
- Servido com `serve -s dist -l 5173` (servidor estático leve)
- Removido `--host` — agora escuta apenas em `127.0.0.1` (acessível via mapeamento de porta do Docker)
- `npm run build` roda durante `docker build` (necessário reinstalar imagem)

**Analogia:** Antes, a loja funcionava no meio da rua com o caixa aberto. Agora, tem parede, porta e só abre na hora certa.

**Vulnerabilidades resolvidas:** M-6, L-4

---

## Resumo técnico

| Componente | Antes (inseguro) | Depois (hardened) |
|---|---|---|
| CORS | `allow_origins=["*"]` | Origens específicas + API Key |
| Autenticação | Nenhuma | API Key via header `X-API-Key` |
| Validação de IP | Nenhuma | `ipaddress.ip_address()` |
| Validação de path | Nenhuma | Whitelist de prefixos |
| Container user | root | `appuser` (non-root) |
| Mounts | Gravitáveis | Read-only (`:ro`) |
| `.dockerignore` | Inexistente | Criado para backend e root |
| `--reload` | Ativado | Removido |
| Exceções na API | `str(e)` completo | Mensagem genérica + log server-side |
| Config sensível | Hardcoded no código | Variáveis de ambiente |
| Mock Zabbix IP | `192.168.1.100` (real) | `192.0.2.1` (RFC 5737) |
| Frontend | Vite dev server | Build de produção + serve |

## Estratégia de Branches (Git Flow Simplificado)

Utilizamos **Git Flow simplificado** com uma branch `develop` como estágio de integração entre as features e a produção.

```
main (produção — sempre estável e deployável)
  └── develop (integração — onde todas as features convergem antes de ir para produção)
        ├── feature/docker-hardening
        ├── feature/input-validation
        ├── feature/config-secrets
        ├── feature/cors-auth
        ├── feature/error-handling
        └── feature/frontend-prod
```

**Regras:**
- `main` é **somente leitura** durante a sprint — nada é commitado diretamente nela
- `develop` é criada a partir de `main` no início da sprint
- Cada feature branch é criada a partir de `develop`
- Features são mergeadas em `develop` após validação individual
- `develop` → `main` é feito ao final da sprint, após validação completa
- Se `develop` acumular problemas, basta não mergeá-la em `main`

### Exceção: release de correção crítica fora do ciclo da sprint

A regra "um release por sprint" tem como propósito **não promover trabalho inacabado**. Quando uma correção crítica é validada como se fosse uma entrega completa — mas só depois do release da sprint — o certo é promover o mesmo assim, e não deixar a `main` carregando o defeito até a sprint seguinte.

Condições para o release fora do ciclo, **todas** obrigatórias:
- o defeito está **validado end-to-end** (a mesma régua dos ACs do §10 do PRD: observado rodando, não só por leitura de código);
- o diff entre `develop` e `main` contém **apenas a correção** — nenhum outro trabalho pendente viaja junto;
- a CI está verde nos dois branch targets;
- o release é um PR de `develop` → `main`, revisado como qualquer outro.

Quando a `develop` **não** cumpre essas condições, a regra geral prevalece: espera-se o fim da sprint. O critério não é a data, é a maturidade da entrega.

> **Por que o caso do #81 (21/10/2026) exigiu essa regra.** O `main` publicado até então somava o banco inteiro no card "Vendas Hoje" (o FR-02 do PRD pede o total **do dia**). O defeito estava **latente**: o simulador da `main` só gerava o dia corrente, então o número saía certo por coincidência — e o bug só apareceria no primeiro banco real, que acumula histórico. Como a próxima sprint nasce da `main` ("`develop` é criada a partir de `main`"), adiar significaria construir a sprint seguinte sobre uma base que promete "Vendas Hoje" e entrega a soma de todos os dias.

### Release sempre com merge commit

O `develop` → `main` é mergeado com **merge commit**, nunca com squash. O squash achata o histórico de uma entrega inteira em um commit e esconde de onde cada mudança veio — foi o que aconteceu no release do É7 (#84), que deixou 23 commits de `develop` sem relação aparente com o `main`. Com merge commit, o `main` mostra a entrega como foi feita, commit a commit.

### Versionamento por tag

Cada release publicado recebe uma **tag anotada** que identifica aquela versão:

```
vMAJOR.MINOR.PATCH
```

| Componente | Sobe quando |
|---|---|
| `MAJOR` | quebra de contrato da API ou da V1 inteira |
| `MINOR` | entrega de funcionalidade nova (épico fechado) |
| `PATCH` | correção de defeito sobre uma versão já lançada |

A tag aponta para o **merge commit do release** na `main` — é ela, e não a branch, que identifica "a versão que está no ar". Sem tag, um release é só um ponteiro de branch: não há como citar, verificar ou reverter uma versão específica.

A primeira tag deste repositório foi criada em 21/10/2026 e retro-rotulou o release do É7 (#84) como `v1.0.0`, para que a numeração não mentisse sobre um release anterior que nunca foi rotulado. Nenhum commit foi reescrito ou movido.

> O `frontend/package.json` está em `0.0.0` (placeholder do Vite) e **não** é o versionamento do produto. O `CHANGELOG` é o diário de bordo (`docs/diario-de-bordo-sprint.md`).

### GitHub: milestone fecha quando o épico fecha

Um milestone é o **container** de um épico. Ele fecha quando **todas as issues dele estiverem fechadas** — e fecha-se **manualmente**, porque o GitHub nunca fecha milestone sozinho.

A distinção que o histórico precisa preservar mora na issue, não no milestone:

| `stateReason` da issue | Significado |
|---|---|
| `completed` | o épico entregou o que prometeu |
| `not_planned` | o épico foi **cancelado** — e o motivo fica registrado no corpo da issue de épico |

Fechar o milestone **não** mexe em nenhuma das issues: o `stateReason` de cada uma é preservado. No caso do É6 (cancelado — "`serve` não agrega valor de estudo sem auth real", PRD §11), a issue de épico #18 continua `not_planned` e a descrição do milestone É7 continua dizendo "Substitui o É6 (cancelado)".

> **Por que essa regra precisa existir (21/10/2026).** Os 7 milestones do É1..É7 estavam **abertos** com **0 issues abertas** e todos os prazos vencidos. O painel de milestones abertos é, por convenção do GitHub, o "o que está em andamento" — e ele dizia **"7 em andamento, todos atrasados"** quando o quadro real era **"0 em andamento"**. Sinal invertido é pior que sinal ausente: treina o olho a ignorar o campo, e faz a lista de milestones parecer um backlog de 7 épicos abertos no momento de planejar o próximo.
>
> A causa não foi descuido de um passo, foi ausência de regra: o repositório fechou **54 de 54** issues com motivo explícito, mas nenhum documento dizia que o container também fecha. A regra foi escrita na mesma hora em que a lacuna apareceu — o mesmo tratamento dado à estratégia de branches, à via de release fora do ciclo e ao versionamento por tag.

**Regra prática, para não esquecer:**
- todas as issues do milestone fechadas → **fecha o milestone**
- épico cancelado → fecha as issues como `not_planned` e fecha o milestone
- épico novo começa com o milestone **aberto** e as issues já ligadas a ele

---

## Branches planejadas

| # | Branch | Entrega | Vulnerabilidades |
|---|---|---|---|
| 1 | `feature/cors-auth` | CORS restrito + API Key | C-1, H-3 |
| 2 | `feature/input-validation` | Validação de IP + sanitização de paths | C-2, M-5 |
| 3 | `feature/docker-hardening` | User não-root, mounts ro, .dockerignore, sem --reload | C-3, H-1, H-4, M-3, M-4 |
| 4 | `feature/error-handling` | Erros genéricos na API | H-2, M-7 |
| 5 | `feature/config-secrets` | Variáveis de ambiente para dados sensíveis | M-1, M-2, H-5, L-3 |
| 6 | `feature/frontend-prod` | Build de produção (não dev server) | M-6, L-4 |

## Prioridade de correção

| Prioridade | IDs | Quando |
|---|---|---|
| Crítico | C-1, C-2, C-3 | Esta sprint (entregas 1, 2, 3) |
| Alto | H-1 a H-5 | Esta sprint (entregas 1, 3, 4, 5) |
| Médio | M-1 a M-7 | Esta sprint (entregas 2, 3, 4, 5, 6) |
| Baixo | L-1 a L-4 | Backlog (L-1, L-2 pendentes) |

## Pendências futuras (não incluídas nesta sprint)

**Todas as 5 foram planejadas em 21/10/2026 e agora vivem no milestone É8** — ver [`docs/sprint-e8-seguranca-evolucao.md`](sprint-e8-seguranca-evolucao.md) e a §12 do PRD. A lista abaixo é mantida só para preservar a rastreabilidade dos códigos L-1/L-2.

| Código antigo | Issue | Onde está agora |
|---|---|---|
| L-1: Excluir dados sensíveis de `mock_data/` do versionamento | [#51](https://github.com/OsirisMariano/analsita/issues/51) | É8 — Épico 1, Onda 1, 6 SP |
| L-2: Configurar TLS/HTTPS via reverse proxy (nginx) | [#52](https://github.com/OsirisMariano/analsita/issues/52) | É8 — Épico 5, Onda 3 (condicionada), 10 SP |
| Autenticação completa com login/senha (esta sprint usa apenas API Key) | [#53](https://github.com/OsirisMariano/analsita/issues/53) | É8 — Épico 2, Onda 1, 20 SP |
| Rate limiting nos endpoints | [#54](https://github.com/OsirisMariano/analsita/issues/54) | É8 — Épico 4, Onda 2, 11 SP |
| Logging estruturado e auditoria de acessos | [#55](https://github.com/OsirisMariano/analsita/issues/55) | É8 — Épico 3, Onda 2, 12 SP |

> **Mudou o conteúdo, não só o paradeiro:** o PRD §11.2 mandava *"reescrever quando as funções estiverem definidas"*. As 5 issues foram reescritas com função, tasks, critérios de aceite e story points.

---

## Product Backlog — Sprint de Segurança

**Metodologia:** Scrum + Kanban
**Capacidade da sprint:** 42 Story Points
**Duração estimada:** 6 dias úteis

---

### Épico 1: CORS + Autenticação — Branch `feature/cors-auth` (8 SP)

| ID | Tarefa | Critérios de aceite | Prioridade | SP | Status |
|---|---|---|---|---|---|
| SEC-01 | Restringir `allow_origins` no CORS | `allow_origins` lista apenas domínios do frontend (não `*`) | P0 | 2 | BACKLOG |
| SEC-02 | Restringir `allow_methods` para `GET` | `allow_methods=["GET"]` | P0 | 1 | BACKLOG |
| SEC-03 | Criar middleware de API Key | Endpoint retorna 403 se header `X-API-Key` ausente ou inválido | P0 | 3 | BACKLOG |
| SEC-04 | Criar variável `API_KEY` no `.env` do backend | `API_KEY=chave-secreta` no `.env.example` | P0 | 1 | BACKLOG |
| SEC-05 | Atualizar `.env.example` do backend | Template com `API_KEY` e `CORS_ORIGINS` | P1 | 1 | BACKLOG |

---

### Épico 2: Validação de Input — Branch `feature/input-validation` (6 SP)

| ID | Tarefa | Critérios de aceite | Prioridade | SP | Status |
|---|---|---|---|---|---|
| SEC-06 | Validar formato de IP em `disparar_ping()` | Usar `ipaddress.ip_address()` — IP inválido retorna `"Erro"` sem chamar subprocess | P0 | 2 | BACKLOG |
| SEC-07 | Criar whitelist de paths em `validador.py` | Constante `ALLOWED_PREFIXES` com `/etc/abastece/`, `/var/abastece/`, `/var/DS_SFTP/` | P1 | 2 | BACKLOG |
| SEC-08 | Validar path antes de ler arquivo | `extrair_valor()` retorna `"acesso_nao_permitido"` se path fora da whitelist | P1 | 1 | BACKLOG |
| SEC-09 | Testar com path malicioso | Request com path `../../etc/shadow` retorna erro genérico | P1 | 1 | BACKLOG |

---

### Épico 3: Docker Hardening — Branch `feature/docker-hardening` (10 SP)

| ID | Tarefa | Critérios de aceite | Prioridade | SP | Status |
|---|---|---|---|---|---|
| SEC-10 | Criar `appuser` no Dockerfile do backend | `groupadd` + `useradd` + `USER appuser` antes do CMD | P0 | 2 | BACKLOG |
| SEC-11 | Criar `appuser` no Dockerfile do frontend | `groupadd` + `useradd` + `USER appuser` antes do CMD | P0 | 2 | BACKLOG |
| SEC-12 | Adicionar `cap_add: [NET_RAW]` no docker-compose | Backend consegue fazer ping com usuário não-root | P0 | 1 | BACKLOG |
| SEC-13 | Tornar mounts read-only no docker-compose | `:ro` em `./backend/app`, `./scripts`, todos os `mock_data/*` | P1 | 1 | BACKLOG |
| SEC-14 | Criar `.dockerignore` no backend | Excluir `.git`, `.env`, `__pycache__`, `*.pyc`, `tests/` | P1 | 1 | BACKLOG |
| SEC-15 | Criar `.dockerignore` na raiz | Excluir `.git`, `node_modules/`, `data/*.db`, `.env` | P1 | 1 | BACKLOG |
| SEC-16 | Remover `--reload` do `entrypoint.sh` | `exec uvicorn app.main:app --host 0.0.0.0 --port 8000` (sem `--reload`) | P1 | 1 | BACKLOG |
| SEC-17 | Testar containers com mounts read-only | Container inicia normalmente, arquivos não modificáveis de dentro | P2 | 1 | BACKLOG |

---

### Épico 4: Error Handling — Branch `feature/error-handling` (4 SP)

| ID | Tarefa | Critérios de aceite | Prioridade | SP | Status |
|---|---|---|---|---|---|
| SEC-18 | Substituir `str(e)` no endpoint `/transacoes` | Retornar `"Erro interno ao acessar o banco de dados"` | P1 | 1 | BACKLOG |
| SEC-19 | Substituir `str(e)` no endpoint `/validacao-dados` | Retornar mensagem genérica, log server-side | P1 | 1 | BACKLOG |
| SEC-20 | Substituir `f"erro_leitura: {e}"` em `validador.py` | Retornar `"erro_leitura"` (sem detalhe), log com `print()` | P1 | 1 | BACKLOG |
| SEC-21 | Verificar se há outros `str(e)` expostos | Grep por `str(e)` e `f"` no `main.py` — nenhum exposto ao cliente | P2 | 1 | BACKLOG |

---

### Épico 5: Configuração + Segredos — Branch `feature/config-secrets` (8 SP)

| ID | Tarefa | Critérios de aceite | Prioridade | SP | Status |
|---|---|---|---|---|---|
| SEC-22 | Externalizar `EQUIPAMENTOS` do `main.py` | Ler de variável de ambiente `EQUIPAMENTOS` (JSON), fallback para valor hardcoded | P1 | 3 | BACKLOG |
| SEC-23 | Externalizar `DB_PATH` | Ler de variável de ambiente `DB_PATH`, fallback para path atual | P1 | 1 | BACKLOG |
| SEC-24 | Externalizar valores de `validacoes_config.py` | `CONVENIADO_CODE`, `NUC_IP`, `SFTP_SERVER` via env vars | P2 | 2 | BACKLOG |
| SEC-25 | Substituir IP do Zabbix no mock | `192.168.1.100` → `192.0.2.1` (RFC 5737) | P1 | 1 | BACKLOG |
| SEC-26 | Criar `.env.example` do backend | Template com todas as variáveis e valores placeholder | P2 | 1 | BACKLOG |

---

### Épico 6: Frontend Produção — Branch `feature/frontend-prod` (6 SP)

| ID | Tarefa | Critérios de aceite | Prioridade | SP | Status |
|---|---|---|---|---|---|
| SEC-27 | Alterar Dockerfile do frontend para build de produção | `RUN npm run build` + `RUN npm install -g serve` | P1 | 2 | BACKLOG |
| SEC-28 | Alterar CMD para `serve` | `CMD ["serve", "-s", "dist", "-l", "5173"]` | P1 | 1 | BACKLOG |
| SEC-29 | Remover `--host` e `args` do docker-compose | Frontend não precisa mais de `args: VITE_API_URL` | P1 | 1 | BACKLOG |
| SEC-30 | Verificar se `.env` funciona em produção | `VITE_API_URL` embutido no build via `docker build --build-arg` | P2 | 1 | BACKLOG |
| SEC-31 | Testar frontend em produção | `http://localhost:5173` carrega normalmente, sem HMR | P2 | 1 | BACKLOG |

---

### Resumo da Sprint

| Épico | Story Points | Branch | Dias estimados |
|---|---|---|---|
| 1 — CORS + Auth | 8 SP | `feature/cors-auth` | Dia 3-4 |
| 2 — Input Validation | 6 SP | `feature/input-validation` | Dia 1-2 |
| 3 — Docker Hardening | 10 SP | `feature/docker-hardening` | Dia 1-2 |
| 4 — Error Handling | 4 SP | `feature/error-handling` | Dia 5 |
| 5 — Config Secrets | 8 SP | `feature/config-secrets` | Dia 3-4 |
| 6 — Frontend Prod | 6 SP | `feature/frontend-prod` | Dia 6 |
| **TOTAL** | **42 SP** | **6 branches** | **6 dias** |

---

### Fluxo Kanban

```
┌─────────────┐    ┌─────────┐    ┌──────────────┐    ┌──────────────────┐    ┌──────────────┐    ┌──────┐
│   BACKLOG   │───▶│  TO DO  │───▶│ IN PROGRESS  │───▶│ MERGE → develop  │───▶│ CODE REVIEW  │───▶│ DONE │
│  (SEC-01..  │    │ (Sprint │    │  (1 devs)    │    │  (feature merge) │    │  (PO rev)    │    │      │
│   SEC-31)   │    │  Plan)  │    │              │    │                  │    │              │    │      │
└─────────────┘    └─────────┘    └──────────────┘    └──────────────────┘    └──────────────┘    └──────┘
                                                                                                       │
                                                                                                       ▼
                                                                                               ┌──────────────┐
                                                                                               │ MERGE → main │
                                                                                               │ (final sprint│
                                                                                               │  ou manual)  │
                                                                                               └──────────────┘
```

**Regras Kanban:**
- No máximo **2 tarefas** em IN PROGRESS por vez
- Feature só vai para MERGE → develop após **validação local** (docker compose up + teste manual)
- Tarefa só vai para DONE após **PO review no develop + teste manual**
- Merge `develop` → `main` é feito **uma única vez ao final da sprint**, após todas as features validadas
- Bloqueios são sinalizados imediatamente

---

### Ordem de Execução Recomendada

```
Pré-sprint:
  Criar branch develop a partir de main

Dia 1-2:  Épico 3 (Docker) + Épico 2 (Input Validation) — paralelos
          └─ SEC-10 a SEC-17 + SEC-06 a SEC-09
          └─ Merge feature → develop

Dia 3-4:  Épico 1 (CORS Auth) + Épico 5 (Config Secrets) — paralelos
          └─ SEC-01 a SEC-05 + SEC-22 a SEC-26
          └─ Merge feature → develop

Dia 5:    Épico 4 (Error Handling) — depende de Épico 1
          └─ SEC-18 a SEC-21
          └─ Merge feature → develop

Dia 6:    Épico 6 (Frontend Prod)
          └─ SEC-27 a SEC-31
          └─ Merge feature → develop
          └─ Validação completa no develop (docker compose up, todos os endpoints)
          └─ Merge develop → main (sprint finalizada)
```

---

### Dependências entre Épicos

```
Épico 3 (Docker)  ──── sem dependências, pode iniciar primeiro
Épico 2 (Input)   ──── sem dependências, pode iniciar primeiro
Épico 1 (CORS)    ──── sem dependências, pode iniciar primeiro
Épico 5 (Config)  ──── sem dependências, pode iniciar primeiro
Épico 4 (Errors)  ──── depende de Épico 1 (mesmo main.py)
Épico 6 (Front)   ──── sem dependências, pode iniciar primeiro
```

---

### Definição de Pronto (Definition of Done)

**Para cada feature individual (DONE por feature):**
- [ ] Código implementado e testado localmente
- [ ] Docker compose up roda sem erros (na feature)
- [ ] Nenhum `str(e)` exposto na API
- [ ] Container roda como não-root
- [ ] Mounts são read-only (exceto `/data`)
- [ ] API Key obrigatória em todos os endpoints
- [ ] PO fez review manual no browser
- [ ] Commit na branch feature correspondente
- [ ] Merge da feature → `develop`

**Para a sprint completa (DONE por sprint):**
- [ ] Todas as 6 features mergeadas em `develop`
- [ ] `docker compose up` completo no `develop` sem erros
- [ ] Teste manual de todos os endpoints no `develop`
- [ ] PO validou o sistema integrado no `develop`
- [ ] Merge `develop` → `main`
- [ ] `main` estável e deployável
- [ ] **Milestone da sprint fechado** (ver "GitHub: milestone fecha quando o épico fecha")
