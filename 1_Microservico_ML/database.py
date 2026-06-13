from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./tickets.db"

# check_same_thread=False é necessário no SQLite para trabalhar com chamadas assíncronas no FastAPI
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Injeção de dependência para instanciar sessões de banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()