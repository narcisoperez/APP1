from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas

def listar_usuarios(db: Session, skip: int = 0, limit: int = 50) -> list[models.Usuario]:
    stmt = select(models.Usuario).offset(skip).limit(limit)
    return list(db.execute(stmt).scalars().all())

def obtener_usuario(db: Session, usuario_id: int) -> models.Usuario | None:
    return db.get(models.Usuario, usuario_id)

def obtener_por_email(db: Session, email: str) -> models.Usuario | None:
    stmt = select(models.Usuario).where(models.Usuario.email == email)
    return db.execute(stmt).scalar_one_or_none()

def crear_usuario(db: Session, data: schemas.UsuarioCreate) -> models.Usuario:
    existente = obtener_por_email(db, data.email)
    if existente:
        raise ValueError("El email ya está registrado")
    usuario = models.Usuario(nombre=data.nombre, email=data.email)
    db.add(usuario)
    db.flush()  # asegura que tenga ID
    db.refresh(usuario)
    return usuario

def actualizar_usuario(db: Session, usuario: models.Usuario, data: schemas.UsuarioUpdate) -> models.Usuario:
    if data.nombre is not None:
        usuario.nombre = data.nombre
    if data.email is not None:
        # Validar unicidad de email si cambia
        if data.email != usuario.email:
            if obtener_por_email(db, data.email):
                raise ValueError("El email ya está registrado")
            usuario.email = data.email
    db.add(usuario)
    db.flush()
    db.refresh(usuario)
    return usuario

def eliminar_usuario(db: Session, usuario: models.Usuario) -> None:
    db.delete(usuario)
    db.flush()