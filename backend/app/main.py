from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import database as dbe #get_db, engine
import models as md #Base
import schemas as sch
import crud as cr


# Crear tablas en el arranque (para SQLite/local dev)
md.Base.metadata.create_all(bind=dbe.engine)

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

@app.get("/usuarios", response_model=List[sch.UsuarioOut])
def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(dbe.get_db),
):
    return cr.listar_usuarios(db, skip=skip, limit=limit)


@app.get("/usuarios/{usuario_id}", response_model=sch.UsuarioOut)
def obtener_usuario(usuario_id: int, db: Session = Depends(dbe.get_db)):
    usuario = cr.obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario


@app.post("/usuarios", response_model=sch.UsuarioOut, status_code=status.HTTP_201_CREATED)
def crear_usuario(payload: sch.UsuarioCreate, db: Session = Depends(dbe.get_db)):
    try:
        return cr.crear_usuario(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.put("/usuarios/{usuario_id}", response_model=sch.UsuarioOut)
def actualizar_usuario(
    usuario_id: int,
    payload: sch.UsuarioUpdate,
    db: Session = Depends(dbe.get_db),
):
    usuario = cr.obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    try:
        return cr.actualizar_usuario(db, usuario, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_usuario(usuario_id: int, db: Session = Depends(dbe.get_db)):
    usuario = cr.obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    cr.eliminar_usuario(db, usuario)
    return None