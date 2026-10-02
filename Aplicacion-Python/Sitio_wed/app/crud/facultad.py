from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import Facultad
from app.schemas.facultad import FacultadCreate


def get(
    db: Session,
    facultad_id: int
) -> Optional[Facultad]:
    return db.get(
        Facultad,
        facultad_id
    )


def get_by_codigo(
    db: Session,
    codigo: int
) -> Optional[Facultad]:
    return (
        db.query(Facultad)
        .filter(Facultad.codigo == codigo)
        .first()
    )


def get_multi(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[Facultad]:
    return (
        db.query(Facultad)
        .order_by(Facultad.id_facultad)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create(
    db: Session,
    esquema: FacultadCreate
) -> Facultad:

    datos = {
        "codigo": esquema.codigo,
        "nombre": esquema.nombre,
        "descripcion": esquema.descripcion,
        "estado": esquema.estado,
    }

    if esquema.id_facultad is not None:
        datos["id_facultad"] = esquema.id_facultad

    facultad = Facultad(**datos)

    db.add(facultad)
    db.commit()
    db.refresh(facultad)

    return facultad
