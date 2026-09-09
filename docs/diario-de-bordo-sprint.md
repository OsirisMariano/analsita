# Diário de Bordo — Sprint V1 Funcional: Segurança

> Arquivo rolante para retomada rápida do trabalho. Dia mais recente no topo.
> Board: https://github.com/users/OsirisMariano/projects/70

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
