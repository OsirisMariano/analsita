# O que foi feito na Sprint V1 Funcional

**Data:** 17/08/2026
**Objetivo:** Transformar o MVP visual em um sistema funcional com dados reais via API

---

## O problema que resolvemos

O dashboard mostrava dados **inventados** (hardcoded). Para ser útil, precisava buscar dados **reais** da API backend.

---

## O que foi construído (6 entregas)

### 1. Variáveis de Ambiente (V.A.R.)

**O que era:** O frontend chamava `http://localhost:8000` direto no código. Dentro do Docker, `localhost` é o próprio container, não o container da API. As chamadas falhavam silenciosamente.

**O que foi feito:** Criamos um arquivo `.env` com a URL da API. O frontend agora lê essa variável. No Docker, usamos `http://api:8000` (nome do container na rede). Fora do Docker, `http://localhost:8000`.

**Analogia:** Era como ligar para o número errado. Agora o telefone está salvo corretamente.

---

### 2. Banco de dados automático

**O que era:** Para testar, era necessário rodar manualmente `python scripts/simulador_posto.py` antes de iniciar o Docker. Sem isso, a API retornava erro 404.

**O que foi feito:** Criamos um `entrypoint.sh` que verifica se o banco existe. Se não existir, roda o simulador automaticamente antes de iniciar a API.

**Analogia:** Antes, precisava "ligar o motor na chave de fenda". Agora, o motor liga sozinho ao girar a chave.

---

### 3. Validação de Arquivos (API + Frontend)

**O que era:** A lista de 15 arquivos de configuração do posto estava **fixa no código do frontend**. Não importava se os arquivos existiam ou não — sempre mostrava "OK".

**O que foi feito:**
- **Backend:** Criamos o endpoint `GET /arquivos` que verifica no disco se cada arquivo existe. Retorna `OK` ou `ERRO` para cada um.
- **Frontend:** O frontend agora busca os dados da API em vez de usar lista fixa.
- **Mocks:** Criamos arquivos fictícios dentro do Docker (`mock_data/`) para simular os arquivos reais do posto.

**Analogia:** Antes, era como uma lista de compras escrita à mão que nunca mudava. Agora, alguém verifica na despensa se cada item realmente existe.

---

### 4. Validação de Dados (API + Frontend)

**O que era:** A verificação de dados de configuração (código do conveniado, IPs, portas, etc.) também estava hardcoded. O frontend mostrava sempre os mesmos resultados.

**O que foi feito:**
- **Backend:** Criamos o endpoint `GET /validacao-dados` que lê os arquivos reais e verifica se os valores estão corretos. Funciona como um sistema de "regras de validação" configurável.
- **Frontend:** O frontend busca os dados da API. O accordion e os badges da sidebar funcionam com dados reais.

**Analogia:** Antes, era como um gabarito fixo de uma prova. Agora, o sistema **aplica a prova** e corrige automaticamente.

---

## Resumo técnico

| Componente | Antes | Depois |
|---|---|---|
| URL da API | Hardcoded `localhost:8000` | Variável de ambiente (`VITE_API_URL`) |
| Banco de dados | Manual (rodar script) | Automático (entrypoint) |
| Validação de arquivos | Dados fixos no frontend | API lê arquivos reais + frontend consome API |
| Validação de dados | Dados fixos no frontend | API valida conteúdo dos arquivos + frontend consome API |
| Mock files | Nenhum | 19 arquivos fictícios em `mock_data/` |

## Arquitetura atual

```
Browser (localhost:5173)
    ↓ fetch (a cada 5s)
API FastAPI (localhost:8000)
    ↓ lê
SQLite (banco de transações)
    ↓ valida
Arquivos de configuração (mock_data/)
```

## Branches criadas

| Branch | Objetivo |
|---|---|
| `feature/variaveis-ambiente` | V.A.R. |
| `feature/db-init` | Banco automático |
| `feature/api-arquivos` | Endpoint de validação de arquivos |
| `feature/frontend-arquivos` | Frontend consome `/arquivos` |
| `feature/api-validacao-dados` | Endpoint de validação de dados |
| `feature/frontend-validacao-dados` | Frontend consome `/validacao-dados` |

## Próximos passos (V2)

- Integração com dados reais do posto (não mocks)
- Autenticação e controle de acesso
- WebSockets (substituir polling)
- Câmeras e leitoras reais
- Histórico e alertas
