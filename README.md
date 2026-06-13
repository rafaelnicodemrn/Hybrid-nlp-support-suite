# Hybrid NLP Support Suite: Real-Time Ticket Triage Ecosystem

Ecossistema corporativo de gerenciamento, triagem e governança inteligente de chamados técnicos utilizando uma arquitetura híbrida de Processamento de Linguagem Natural (NLP) e Inteligência Artificial Generativa.

## Arquitetura do Sistema e Roteamento Híbrido

O sistema implementa uma esteira de tomada de decisão em duas camadas para otimização de latência, controle de custos e tratamento de exceções complexas (sarcasmo/ironia):

1. **Camada Local (Inferência Determinística)**: Baseada em um modelo Transformer bidirecional (`RoBERTuito-BERT`) encapsulado via FastAPI. Classifica o sentimento do ticket em milissegundos com custo zero de nuvem.
2. **Camada Cloud (Auditoria Generativa)**: Ativada dinamicamente via arquitetura HITL se o score de confiança do modelo local decair abaixo do Threshold de 65% ou se o sentimento for explicitamente Negativo. O modelo `gemini-3.5-flash` assume a requisição de forma assíncrona, definindo níveis de prioridade operacional e gerando rascunhos de respostas empáticas.

## Stack Tecnológica

* **Backend**: Python 3.11, FastAPI, Uvicorn, SQLAlchemy ORM, SQLite.
* **Core IA**: HuggingFace Transformers (`pysentimiento/robertuito-sentiment-analysis`), Google GenAI SDK.
* **Frontend/Dashboard**: Streamlit, Pandas, Requests.
* **DevOps/Infra**: Docker, Docker Compose (com Healthchecks nativos), Build-time Caching.

## Inicialização Rápida (Windows)

```bash
# Inicializa os containers do backend e a interface visual Streamlit automaticamente
.\iniciar_tudo.bat
# Para encerrar os serviços de forma segura
.\parar_tudo.bat