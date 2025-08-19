from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# Salida (lo que devolvemos)
class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    creado_en: datetime

    model_config = {"from_attributes": True}

# Entrada para crear
class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=120)
    email: EmailStr

# Entrada para actualizar (parcial o total)
class UsuarioUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=120)
    email: EmailStr | None = None