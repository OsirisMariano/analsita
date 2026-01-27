# Analista SemParar - Dashboard MVP 🚀

Este projeto é uma solução de monitoramento de infraestrutura de pista para o sistema de abastecimento SemParar. Ele transforma a lógica de diagnóstico baseada em terminal em uma interface visual moderna, facilitando a identificação proativa de falhas.

## 🎯 Objetivo da V1 (MVP)
A primeira versão foca na centralização dos dados críticos coletados pelo motor de análise, substituindo a leitura manual de logs por indicadores visuais.

### Entregáveis:
- **Status de Conectividade:** Monitoramento em tempo real (Online/Offline) das Antenas e Sensores de cada lado da pista.
- **Painel de Abastecimentos:** Contador de transações do dia extraído diretamente do banco SQLite.
- **Diagnóstico de VPAR:** Verificação automatizada de status de licenças e funcionamento do software de reconhecimento de placas.
- **Saúde do Sistema:** Alertas sobre equipamentos travados ou falhas de comunicação recorrentes.

## 🛠️ Stack Tecnológica
- **Backend:** Python com FastAPI (Processamento de dados e integração com SQLite).
- **Frontend:** Vue.js + Tailwind CSS (Interface administrativa baseada no TailAdmin).
- **Infraestrutura:** Docker & Docker Compose (Ambiente isolado e replicável).

---
*Este é um projeto de desenvolvimento ágil para otimização do suporte técnico operacional.*