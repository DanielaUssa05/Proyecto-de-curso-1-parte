from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.models import AuditoriaEvento


# =========================================================
# REGISTRAR AUDITORÍA
# =========================================================

def registrar(
    db: Session,
    *,
    entidad: str,
    entidad_id: int,
    accion: str,
    id_usuario: Optional[int] = None,
    descripcion: Optional[Dict[str, Any]] = None,
) -> AuditoriaEvento:

    # id_usuario representa QUIÉN realizó la acción.
    #
    # Para las acciones realizadas desde FastAPI:
    # - Secretaria que habilita/deshabilita usuario
    # - Usuario que realiza otra acción
    #
    # Esto es diferente de los triggers de MySQL de reservas,
    # que pueden guardar el usuario propietario de la reserva.

    evento = AuditoriaEvento(
        id_usuario=id_usuario,
        entidad=entidad,
        fecha_y_hora=datetime.now(),
        tipoAccion=accion,
        descripcion=descripcion,
    )

    db.add(evento)

    return evento


# =========================================================
# LISTAR HISTORIAL DE AUDITORÍA
# =========================================================

def listar(
    db: Session,
    entidad: Optional[str] = None,
    accion: Optional[str] = None,
    id_usuario: Optional[int] = None,
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[AuditoriaEvento]:

    q = db.query(AuditoriaEvento)

    # -----------------------------------------------------
    # FILTRO POR ENTIDAD
    # -----------------------------------------------------

    if entidad:
        q = q.filter(
            AuditoriaEvento.entidad == entidad
        )

    # -----------------------------------------------------
    # FILTRO POR TIPO DE ACCIÓN
    # -----------------------------------------------------

    if accion:
        q = q.filter(
            AuditoriaEvento.tipoAccion == accion
        )

    # -----------------------------------------------------
    # FILTRO POR USUARIO QUE REALIZÓ LA ACCIÓN
    # -----------------------------------------------------

    if id_usuario:
        q = q.filter(
            AuditoriaEvento.id_usuario == id_usuario
        )

    # -----------------------------------------------------
    # FILTRO DESDE
    # -----------------------------------------------------

    if desde:
        q = q.filter(
            AuditoriaEvento.fecha_y_hora >= desde
        )

    # -----------------------------------------------------
    # FILTRO HASTA
    # -----------------------------------------------------

    if hasta:
        q = q.filter(
            AuditoriaEvento.fecha_y_hora <= hasta
        )

    # -----------------------------------------------------
    # ORDEN DEL HISTORIAL
    # -----------------------------------------------------
    #
    # Primero aparecen las acciones más recientes.
    #
    # id_auditoria DESC sirve como segundo criterio para
    # mantener un orden estable cuando dos acciones tienen
    # exactamente la misma fecha/hora.

    return (
        q.order_by(
            AuditoriaEvento.fecha_y_hora.desc(),
            AuditoriaEvento.id_auditoria.desc(),
        )
        .offset(skip)
        .limit(limit)
        .all()
    )