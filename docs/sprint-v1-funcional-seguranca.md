# Sprint V1 Funcional — Segurança

**Data:** 18/08/2026
**Objetivo:** Corrigir brechas de segurança identificadas na auditoria da Sprint V1 Funcional

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

**O que era:** O container do frontend rodava `vite dev` (servidor de desenvolvimento) com `--host`. O Vite dev expõe HMR WebSocket (execução de código arbitrário), error overlays com snippets de código, e roda显著 mais lento. O `--host` bindava em `0.0.0.0`, acessível de qualquer máquina na rede.

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

- L-1: Excluir dados sensíveis de `mock_data/` do versionamento
- L-2: Configurar TLS/HTTPS via reverse proxy (nginx)
- Autenticação completa com login/senha (esta sprint usa apenas API Key)
- Rate limiting nos endpoints
- Logging estruturado e auditoria de acessos

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
┌─────────────┐    ┌─────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────┐
│   BACKLOG   │───▶│  TO DO  │───▶│ IN PROGRESS  │───▶│ CODE REVIEW │───▶│ DONE │
│  (SEC-01..  │    │ (Sprint │    │  (1 devs)    │    │  (PO rev)   │    │      │
│   SEC-31)   │    │  Plan)  │    │              │    │             │    │      │
└─────────────┘    └─────────┘    └──────────────┘    └─────────────┘    └──────┘
```

**Regras Kanban:**
- No máximo **2 tarefas** em IN PROGRESS por vez
- Tarefa só vai para DONE após **PO review + teste manual**
- Bloqueios são sinalizados imediatamente

---

### Ordem de Execução Recomendada

```
Dia 1-2:  Épico 3 (Docker) + Épico 2 (Input Validation) — paralelos
          └─ SEC-10 a SEC-17 + SEC-06 a SEC-09

Dia 3-4:  Épico 1 (CORS Auth) + Épico 5 (Config Secrets) — paralelos
          └─ SEC-01 a SEC-05 + SEC-22 a SEC-26

Dia 5:    Épico 4 (Error Handling) — depende do main.py limpo
          └─ SEC-18 a SEC-21

Dia 6:    Épico 6 (Frontend Prod) + merge final
          └─ SEC-27 a SEC-31 → merge todas na main
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

- [ ] Código implementado e testado localmente
- [ ] Docker compose up roda sem erros
- [ ] Nenhum `str(e)` exposto na API
- [ ] Container roda como não-root
- [ ] Mounts são read-only (exceto `/data`)
- [ ] API Key obrigatória em todos os endpoints
- [ ] PO fez review manual no browser
- [ ] Commit na branch correspondente
- [ ] Merge na main após review
