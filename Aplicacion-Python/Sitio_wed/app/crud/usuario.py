from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Usuario


def get_by_correo(db: Session, correo: str):
    return (
        db.query(Usuario)
        .filter(Usuario.correo_institucional == correo)
        .first()
    )


def get_by_id(db: Session, usuario_id: int):
    return (
        db.query(Usuario)
        .filter(Usuario.id_usuario == usuario_id)
        .first()
    )


def get_all(db: Session):
    return db.query(Usuario).all()


def get_multi(
    db: Session,
    facultad_id: int | None = None,
    rol: str | None = None,
    estado: str | None = None,
):
    query = db.query(Usuario)

    if facultad_id is not None:
        query = query.filter(Usuario.id_facultad == facultad_id)

    if rol is not None:
        query = query.filter(Usuario.rol == rol)

    if estado is not None:
        query = query.filter(Usuario.estado == estado)

    return query.all()


def get(db: Session, usuario_id: int):
    return (
        db.query(Usuario)
        .filter(Usuario.id_usuario == usuario_id)
        .first()
    )


def create(db: Session, esquema):
    usuario = Usuario(
        id_facultad=esquema.id_facultad,
        nombre_completo=esquema.nombre_completo,
        correo_institucional=esquema.correo_institucional,
        rol=esquema.rol,
        estado="Activo",
        fecha_creacion=datetime.now(),
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


def update(db: Session, usuario: Usuario, esquema):
    if esquema.nombre_completo is not None:
        usuario.nombre_completo = esquema.nombre_completo

    if esquema.rol is not None:
        usuario.rol = esquema.rol

    db.commit()
    db.refresh(usuario)

    return usuario