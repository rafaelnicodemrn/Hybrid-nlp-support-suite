import time
import logging
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Importando os nossos próprios módulos da Clean Architecture
from database import get_db
from models import TicketDB
from schemas import TicketRequest, TicketResponse
from services import ml_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NLP Support Engine | Clean Architecture",
    description="Engine assíncrona corporativa combinando classificação local (RoBERTuito) e auditoria por LLM (Gemini).",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Monitoramento"])
async def health_check():
    """Endpoint utilitário para orquestradores de contêineres e healthchecks."""
    return {"status": "operacional", "timestamp": time.time()}

@app.get("/api/v1/tickets", tags=["Administração"])
async def get_all_tickets(db: Session = Depends(get_db)):
    """Recupera todos os logs consolidados para o dashboard analítico."""
    try:
        return db.query(TicketDB).all()
    except Exception as e:
        logger.error(f"Erro ao ler banco de dados: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao acessar o banco relacional.")

@app.post("/api/v1/analyze", response_model=TicketResponse, status_code=status.HTTP_200_OK, tags=["Análise"])
async def process_ticket(request: TicketRequest, db: Session = Depends(get_db)):
    start_time = time.time()
    
    # --- Passo 1: Inferência de Sentimento com IA Local (BERT) ---
    try:
        sentiment, confidence = ml_service.analyze_local(request.text)
    except Exception:
        raise HTTPException(status_code=500, detail="Falha no modelo de NLP local.")

    insight = "N/A"
    routed = False
    priority_level = "NORMAL"

    # --- Passo 2: Roteamento Híbrido Condicional ---
    if sentiment == "NEG" or confidence < 0.65:
        routed = True
        logger.info("Gatilho ativado! Roteando requisição para auditoria na nuvem externa.")
        priority_level, insight = await ml_service.get_llm_insight(request.text, sentiment)

    # --- Passo 3: Persistência no SQLite ---
    try:
        db_ticket = TicketDB(
            text=request.text,
            sentiment=sentiment,
            confidence_score=round(confidence, 4),
            insight=insight,
            priority=priority_level,
            routed_to_llm=routed
        )
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
    except Exception as e:
        logger.error(f"Falha de gravação de logs: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro operacional ao persistir logs no banco.")

    processing_time_ms = (time.time() - start_time) * 1000

    return TicketResponse(
        id=db_ticket.id,
        text=db_ticket.text,
        sentiment=db_ticket.sentiment,
        confidence_score=db_ticket.confidence_score,
        insight=db_ticket.insight,
        priority=db_ticket.priority,
        routed_to_llm=db_ticket.routed_to_llm,
        processing_time_ms=round(processing_time_ms, 2)
    )