from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    creado_en = Column(DateTime, default=datetime.utcnow, nullable=False)