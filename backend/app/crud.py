from sqlalchemy.orm import Session
from sqlalchemy import select
import models as md
import schemas as sch

def listar_usuarios(db: Session, skip: int = 0, limit: int = 50) -> list[md.Usuario]:
    stmt = select(md.Usuario).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())

def obtener_usuario(db: Session, usuario_id: int) -> md.Usuario | None:
    return db.get(md.Usuario, usuario_id)

def obtener_por_email(db: Session, email: str) -> md.Usuario | None:
    stmt = select(md.Usuario).where(md.Usuario.email == email)
    return db.execute(stmt).scalar_one_or_none()

def crear_usuario(db: Session, data: sch.UsuarioCreate) -> md.Usuario:
    existente = obtener_por_email(db, data.email)
    if existente:
        raise ValueError("El email ya está registrado")
    usuario = md.Usuario(nombre=data.nombre, email=data.email)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def actualizar_usuario(db: Session, usuario: md.Usuario, data: sch.UsuarioUpdate) -> md.Usuario:
    if data.nombre is not None:
        usuario.nombre = data.nombre
    if data.email is not None:
        # Validar unicidad de email si cambia
        if data.email != usuario.email:
            if obtener_por_email(db, data.email):
                raise ValueError("El email ya está registrado")
            usuario.email = data.email
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def eliminar_usuario(db: Session, usuario: md.Usuario) -> None:
    db.delete(usuario)