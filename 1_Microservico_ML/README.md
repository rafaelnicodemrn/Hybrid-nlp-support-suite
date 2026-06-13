# 🧠 NLP Support Ticket API (v2.0.0)

Este microsserviço é o núcleo de processamento de linguagem natural do Projeto NLP. Ele utiliza uma arquitetura híbrida que combina modelos locais rápidos com Large Language Models (LLMs) potentes.

## 🚀 Arquitetura e Fluxo de Dados

O serviço segue os princípios de Clean Architecture, dividido em módulos:

1.  **`database.py`**: Configuração do SQLite e persistência ORM.
2.  **`models.py`**: Definição das entidades de banco de dados.
3.  **`schemas.py`**: Contratos de entrada e saída (Pydantic).
4.  **`services.py`**: Lógica de negócio e integração com IA (BERT + Gemini).
5.  **`main.py`**: Orquestração de rotas e middleware.

### Fluxo de Análise:
- **Passo 1**: O texto é recebido via API REST.
- **Passo 2**: O modelo **RoBERTuito** (BERT) local classifica o sentimento.
- **Passo 3**: Se o sentimento for **Negativo** ou a **Confiança < 65%**, o sistema roteia o ticket para o **Google Gemini 1.5 Flash**.
- **Passo 4**: O resultado é persistido no banco de dados e retornado ao cliente.

## 🛠️ Tecnologias Utilizadas

- **FastAPI**: Framework web de alta performance.
- **SQLAlchemy**: ORM para manipulação de dados.
- **Transformers (HuggingFace)**: Motor de NLP local.
- **Google GenAI SDK**: Integração com Gemini.
- **Docker & Docker Compose**: Containerização e orquestração.

## 📦 Como Executar

### Pré-requisitos
- Docker e Docker Compose instalados.
- Chave de API do Google (Gemini) configurada no arquivo `.env`.

### Via Docker (Recomendado)
```bash
docker-compose up -d --build
```

### Endpoints Principais
- `GET /health`: Verificação de saúde do sistema.
- `POST /api/v1/analyze`: Envio de texto para análise.
- `GET /api/v1/tickets`: Listagem do histórico de processamento.
- `GET /docs`: Documentação interativa Swagger.

## 🛡️ Segurança e Boas Práticas
- **Non-root user**: O container roda com um usuário seguro sem privilégios de administrador.
- **Build-time Cache**: O modelo de IA é baixado durante o build para garantir rapidez no startup.
- **Graceful Degradation**: Se a LLM externa falhar, o sistema continua operando com os dados locais.
