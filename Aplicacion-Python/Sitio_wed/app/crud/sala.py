from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Recurso, Sala
from app.schemas.sala import RecursoCreate, SalaCreate, SalaUpdate


def get(db: Session, sala_id: int) -> Optional[Sala]:
    return db.get(Sala, sala_id)


def get_by_codigo(db: Session, codigo: int) -> Optional[Sala]:
    return db.query(Sala).filter(Sala.codigo == codigo).first()


def get_multi(db: Session, facultad_id: Optional[int] = None, estado: Optional[str] = None,
            skip: int = 0, limit: int = 100) -> List[Sala]:
    q = db.query(Sala)
    if facultad_id:
        q = q.filter(Sala.id_facultad == facultad_id)
    if estado:
        q = q.filter(Sala.estado == estado)
    return q.offset(skip).limit(limit).all()


def create(db: Session, esquema: SalaCreate) -> Sala:
    sala = Sala(id_facultad=esquema.id_facultad, codigo=esquema.codigo,
                nombre=esquema.nombre, estado="Habilitada",
                observaciones=esquema.observaciones)
    db.add(sala)
    db.commit()
    db.refresh(sala)
    return sala


def update(db: Session, sala: Sala, esquema: SalaUpdate) -> Sala:
    if esquema.nombre is not None:
        sala.nombre = esquema.nombre
    if esquema.observaciones is not None:
        sala.observaciones = esquema.observaciones
    db.commit()
    db.refresh(sala)
    return sala


def listar_recursos(db: Session, sala_id: int) -> List[Recurso]:
    return db.query(Recurso).filter(Recurso.id_sala == sala_id).all()


def crear_recurso(db: Session, sala_id: int, esquema: RecursoCreate) -> Recurso:
    recurso = Recurso(id_sala=sala_id, nombre_recurso=esquema.nombre_recurso,
                    descripcion=esquema.descripcion)
    db.add(recurso)
    db.commit()
    db.refresh(recurso)
    return recurso