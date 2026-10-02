from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import auditoria as crud_auditoria
from app.schemas.auditoria import AuditoriaOut


router = APIRouter()


# =========================================================
# HISTORIAL DE AUDITORÍA
# =========================================================

@router.get(
    "",
    response_model=List[AuditoriaOut]
)
def listar_eventos(
    entidad: Optional[str] = None,
    accion: Optional[str] = None,
    usuarioId: Optional[int] = None,
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Devuelve el historial de auditoría.

    Permite filtrar por:

    - entidad: usuario, reserva o sala
    - accion: Habilitar, Deshabilitar, Actualizar o Eliminar
    - usuarioId: usuario que realizó la acción
    - desde: fecha/hora inicial
    - hasta: fecha/hora final
    """

    return crud_auditoria.listar(
        db,
        entidad=entidad,
        accion=accion,
        id_usuario=usuarioId,
        desde=desde,
        hasta=hasta,
        skip=skip,
        limit=limit,
    )