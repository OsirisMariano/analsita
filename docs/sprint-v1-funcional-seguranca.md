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
