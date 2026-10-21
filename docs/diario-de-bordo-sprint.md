# Diário de Bordo — Sprint V1 Funcional: Segurança

> Arquivo rolante para retomada rápida do trabalho. Dia mais recente no topo.
> Board: https://github.com/users/OsirisMariano/projects/70

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
