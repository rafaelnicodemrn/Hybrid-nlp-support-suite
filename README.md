# 🎫 Hybrid NLP Support Suite

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![HuggingFace](https://img.shields.io/badge/%F0%9F%A4%97%20Transformers-FFD21E)
![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?logo=googlegemini&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

Triagem de chamados de suporte em tempo real, com **arquitetura híbrida**: um modelo Transformer local classifica o sentimento em milissegundos e, só quando necessário, uma IA generativa na nuvem audita o ticket, define a prioridade e redige uma resposta empática.

## 🧭 Como funciona

```
Ticket ──► FastAPI ──► RoBERTuito (local, custo zero)
                            │
              confiança ≥ 65% e sentimento não negativo?
                  │ sim                      │ não
                  ▼                          ▼
            resultado direto        Gemini (nuvem): prioridade + rascunho de resposta
                  └───────────┬──────────────┘
                              ▼
                     SQLite  ──►  Dashboard Streamlit
```

1. **Camada local:** `pysentimiento/robertuito-sentiment-analysis` via Transformers, sem custo de nuvem e com baixa latência.
2. **Camada cloud (HITL):** acionada quando a confiança fica abaixo de **65%** ou o sentimento é **negativo** (casos como sarcasmo e ironia). O Gemini define a prioridade operacional e gera o rascunho da resposta.
3. **Persistência e visualização:** resultados salvos com SQLAlchemy/SQLite e exibidos em um dashboard.

## 🛠️ Stack

| Camada | Tecnologias |
|---|---|
| Backend | Python 3.11, FastAPI, Uvicorn, SQLAlchemy, SQLite, Pydantic |
| IA | HuggingFace Transformers (RoBERTuito), Google GenAI SDK |
| Frontend | Streamlit, Pandas, Requests |
| Infra | Docker, Docker Compose (com *healthcheck*) |

## 📁 Estrutura

```
├── 1_Microservico_ML/      # API de análise (FastAPI + modelos + Docker)
│   ├── main.py             # rotas
│   ├── services.py         # BERT local + Gemini
│   ├── models.py / schemas.py / database.py
│   └── docker-compose.yml
├── 2_Interface_Visual/     # Dashboard Streamlit
│   └── app_ui.py
├── iniciar_tudo.bat        # sobe API e dashboard (Windows)
├── parar_tudo.bat
└── *.pdf                   # documentação acadêmica do projeto
```

## 🚀 Como executar

Crie `1_Microservico_ML/.env` com a sua chave do Gemini:

```env
GOOGLE_API_KEY=sua_chave_aqui
```

**Windows (tudo de uma vez):**

```bash
.\iniciar_tudo.bat
.\parar_tudo.bat   # para encerrar
```

**Só a API, via Docker:**

```bash
cd 1_Microservico_ML
docker-compose up -d --build
```

### Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/v1/analyze` | Analisa o texto de um ticket |
| `GET` | `/api/v1/tickets` | Lista tickets já analisados |
| `GET` | `/health` | Verificação de saúde |

A documentação interativa fica em `http://localhost:8000/docs` (porta 8000).

## 📚 Documentação

- *Inteligência Artificial na Triagem de Suporte* (PDF)
- *Documento Resumo Acadêmico, NLP Support Suite* (PDF)
