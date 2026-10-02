from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_usuario_opcional
from app.crud import reserva as crud_reserva
from app.crud import sala as crud_sala
from app.models import Usuario
from app.schemas.reserva import (
    DisponibilidadOut,
    ReservaAjuste,
    ReservaCreate,
    ReservaOut,
)
from app.services import reserva_service


router = APIRouter()


@router.get(
    "/disponibilidad",
    response_model=DisponibilidadOut
)
def consultar_disponibilidad(
    facultadId: int,
    fecha: date,
    db: Session = Depends(get_db)
):
    return reserva_service.consultar_disponibilidad(
        db,
        facultadId,
        fecha
    )


@router.post(
    "",
    response_model=ReservaOut,
    status_code=201
)
def crear_reserva(
    usuarioId: int,
    facultadId: int,
    salaId: int,
    esquema: ReservaCreate,
    db: Session = Depends(get_db),
):
    usuario = db.get(Usuario, usuarioId)

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="El usuario no existe."
        )

    return reserva_service.crear_reserva(
        db,
        esquema,
        usuario,
        facultadId,
        salaId
    )


@router.get(
    "/mias",
    response_model=List[ReservaOut]
)
def mis_reservas(
    usuarioId: int,
    db: Session = Depends(get_db)
):
    return crud_reserva.listar_por_usuario(
        db,
        usuarioId
    )


@router.get(
    "",
    response_model=List[ReservaOut]
)
def listar_reservas(
    facultadId: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    if skip < 0:
        raise HTTPException(
            status_code=400,
            detail="skip no puede ser negativo."
        )

    if limit <= 0:
        raise HTTPException(
            status_code=400,
            detail="limit debe ser mayor que 0."
        )

    return crud_reserva.listar_por_facultad(
        db,
        facultadId,
        skip,
        limit
    )


@router.put(
    "/{reserva_id}/cancelar",
    response_model=ReservaOut
)
def cancelar_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    usuario: Optional[Usuario] = Depends(get_usuario_opcional)
):
    return reserva_service.cancelar_reserva(
        db,
        reserva_id,
        usuario
    )


@router.put(
    "/{reserva_id}/ajustar",
    response_model=ReservaOut
)
def ajustar_reserva(
    reserva_id: int,
    esquema: ReservaAjuste,
    db: Session = Depends(get_db),
    usuario: Optional[Usuario] = Depends(get_usuario_opcional)
):
    return reserva_service.ajustar_reserva(
        db,
        reserva_id,
        esquema,
        usuario
    )