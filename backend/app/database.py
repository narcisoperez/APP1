from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite (archivo local). Cambia por tu URL real si usas Postgres/MySQL.
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# check_same_thread=False es necesario para SQLite con múltiples hilos (Uvicorn)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session local por request
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

@contextmanager
def session_scope():
    """Context manager para manejar la sesion y commits/rollbacks de forma segura."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()