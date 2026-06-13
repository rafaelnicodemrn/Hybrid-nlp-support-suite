from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base, engine

class TicketDB(Base):
    """Modelo ORM que define a estrutura da tabela de logs e métricas."""
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String, index=True)
    sentiment = Column(String)
    confidence_score = Column(Float)
    insight = Column(String)
    priority = Column(String, default="NORMAL") 
    routed_to_llm = Column(Boolean)

# Cria as tabelas automaticamente quando o sistema sobe
Base.metadata.create_all(bind=engine)