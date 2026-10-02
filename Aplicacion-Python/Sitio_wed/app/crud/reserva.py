from datetime import date, time
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.constants import ESTADOS_RESERVA_VIGENTES
from app.models import Reserva, Sala


def get(
    db: Session,
    reserva_id: int
) -> Optional[Reserva]:
    return db.get(
        Reserva,
        reserva_id
    )


def existe_solapamiento(
    db: Session,
    id_sala: int,
    fecha: date,
    hora_inicio: time,
    hora_fin: time,
    excluir_id: Optional[int] = None
) -> bool:

    # Regla de negocio R2:
    # no puede haber dos reservas vigentes
    # que se crucen en la misma sala.

    q = db.query(Reserva).filter(
        Reserva.id_sala == id_sala,
        Reserva.fecha == fecha,
        Reserva.estado.in_(ESTADOS_RESERVA_VIGENTES),
        Reserva.hora_inicio < hora_fin,
        Reserva.hora_fin > hora_inicio,
    )

    if excluir_id is not None:
        q = q.filter(
            Reserva.id_reserva != excluir_id
        )

    return db.query(q.exists()).scalar()


def listar_ocupadas(
    db: Session,
    id_sala: int,
    fecha: date
) -> List[Reserva]:

    return (
        db.query(Reserva)
        .filter(
            Reserva.id_sala == id_sala,
            Reserva.fecha == fecha,
            Reserva.estado.in_(ESTADOS_RESERVA_VIGENTES)
        )
        .order_by(Reserva.hora_inicio)
        .all()
    )


def listar_por_usuario(
    db: Session,
    id_usuario: int
) -> List[Reserva]:

    return (
        db.query(Reserva)
        .filter(
            Reserva.id_usuario == id_usuario
        )
        .order_by(
            Reserva.fecha.desc(),
            Reserva.hora_inicio
        )
        .all()
    )


def listar_por_facultad(
    db: Session,
    id_facultad: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Reserva]:

    q = (
        db.query(Reserva)
        .join(
            Sala,
            Reserva.id_sala == Sala.id_sala
        )
    )

    if id_facultad is not None:
        q = q.filter(
            Sala.id_facultad == id_facultad
        )

    return (
        q.order_by(
            Reserva.fecha,
            Reserva.hora_inicio
        )
        .offset(skip)
        .limit(limit)
        .all()
    )