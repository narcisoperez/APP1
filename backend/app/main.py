from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .database import get_db, engine
from .models import Base
from . import crud, schemas

# Crear tablas en el arranque (para SQLite/local dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Usuarios API", version="1.0.0")

# CORS (ajusta orígenes según tu front)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # pon tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Rutas /usuarios
# -------------------------------

@app.get("/usuarios", response_model=List[schemas.UsuarioOut])
def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    return crud.listar_usuarios(db, skip=skip, limit=limit)


@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioOut)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud.obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario


@app.post("/usuarios", response_model=schemas.UsuarioOut, status_code=status.HTTP_201_CREATED)
def crear_usuario(payload: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return crud.crear_usuario(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioOut)
def actualizar_usuario(
    usuario_id: int,
    payload: schemas.UsuarioUpdate,
    db: Session = Depends(get_db),
):
    usuario = crud.obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    try:
        return crud.actualizar_usuario(db, usuario, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = crud.obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    crud.eliminar_usuario(db, usuario)
    return None