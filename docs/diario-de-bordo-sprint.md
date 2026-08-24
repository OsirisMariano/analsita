# Diário de Bordo — Sprint V1 Funcional: Segurança

> Arquivo rolante para retomada rápida do trabalho. Dia mais recente no topo.
> Board: https://github.com/users/OsirisMariano/projects/70

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
