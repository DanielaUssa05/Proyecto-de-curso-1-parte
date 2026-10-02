from datetime import date, time, timedelta
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.constants import (
    AccionAuditoria,
    EntidadAuditoria,
    EstadoReserva,
    EstadoSala,
    Rol,
)
from app.crud import auditoria as crud_auditoria
from app.crud import reserva as crud_reserva
from app.models import Reserva, Sala, Usuario
from app.schemas.reserva import (
    DisponibilidadOut,
    DisponibilidadSalaOut,
    FranjaDisponible,
    FranjaOcupada,
    ReservaAjuste,
    ReservaCreate,
)


def _parse_hora(valor: str) -> time:
    h, m = valor.split(":")
    return time(int(h), int(m))


HORA_APERTURA = _parse_hora(settings.HORA_APERTURA)
HORA_CIERRE = _parse_hora(settings.HORA_CIERRE)


def _payload(reserva: Reserva) -> dict:
    return {
        "id_reserva": reserva.id_reserva,
        "id_sala": reserva.id_sala,
        "id_usuario": reserva.id_usuario,
        "fecha": str(reserva.fecha),
        "hora_inicio": str(reserva.hora_inicio),
        "hora_fin": str(reserva.hora_fin),
        "estado": reserva.estado,
    }


def _validar_horario(
    hora_inicio: time,
    hora_fin: time
) -> None:

    # Regla de negocio R1:
    # horario institucional 7:00 a.m. - 9:30 p.m.

    if (
        hora_inicio < HORA_APERTURA
        or hora_fin > HORA_CIERRE
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "La reserva debe estar dentro del horario institucional "
                f"({settings.HORA_APERTURA} a {settings.HORA_CIERRE})."
            ),
        )

    if hora_fin <= hora_inicio:
        raise HTTPException(
            status_code=400,
            detail=(
                "La hora de fin debe ser mayor "
                "que la hora de inicio."
            )
        )


def _verificar_acceso_facultad(
    usuario: Usuario,
    id_facultad: int
) -> None:

    if usuario.id_facultad != id_facultad:
        raise HTTPException(
            status_code=403,
            detail=(
                "El usuario no pertenece a la facultad "
                "seleccionada."
            )
        )


def _generar_franjas() -> list[tuple[time, time]]:
    franjas = []

    actual = datetime_completa(
        HORA_APERTURA
    )

    cierre = datetime_completa(
        HORA_CIERRE
    )

    while actual + timedelta(minutes=30) <= cierre:
        inicio = actual.time()
        fin = (
            actual + timedelta(minutes=30)
        ).time()

        franjas.append(
            (inicio, fin)
        )

        actual += timedelta(minutes=30)

    return franjas


def datetime_completa(hora: time):
    from datetime import datetime

    return datetime.combine(
        date.today(),
        hora
    )


def _franja_ocupada(
    inicio: time,
    fin: time,
    ocupadas: list[Reserva]
) -> bool:

    for reserva in ocupadas:
        if (
            reserva.hora_inicio < fin
            and reserva.hora_fin > inicio
        ):
            return True

    return False


def consultar_disponibilidad(
    db: Session,
    facultad_id: int,
    fecha: date
) -> DisponibilidadOut:

    salas = (
        db.query(Sala)
        .filter(
            Sala.id_facultad == facultad_id,
            Sala.estado == EstadoSala.HABILITADA.value
        )
        .order_by(Sala.id_sala)
        .all()
    )

    if not salas:
        raise HTTPException(
            status_code=404,
            detail=(
                "No hay salas habilitadas "
                "en la facultad seleccionada."
            )
        )

    resultado_salas = []

    for sala in salas:

        ocupadas = crud_reserva.listar_ocupadas(
            db,
            sala.id_sala,
            fecha
        )

        franjas = _generar_franjas()

        disponibles = []

        for inicio, fin in franjas:

            if not _franja_ocupada(
                inicio,
                fin,
                ocupadas
            ):
                disponibles.append(
                    FranjaDisponible(
                        hora_inicio=inicio,
                        hora_fin=fin
                    )
                )

        resultado_salas.append(
            DisponibilidadSalaOut(
                id_sala=sala.id_sala,
                codigo=sala.codigo,
                nombre=sala.nombre,
                estado=sala.estado,
                ocupadas=[
                    FranjaOcupada(
                        hora_inicio=reserva.hora_inicio,
                        hora_fin=reserva.hora_fin,
                        estado=reserva.estado
                    )
                    for reserva in ocupadas
                ],
                disponibles=disponibles
            )
        )

    return DisponibilidadOut(
        id_facultad=facultad_id,
        fecha=fecha,
        salas=resultado_salas
    )


def crear_reserva(
    db: Session,
    esquema: ReservaCreate,
    usuario: Usuario,
    facultad_id: int,
    sala_id: int
) -> Reserva:

    # =====================================================
    # VALIDAR USUARIO
    # =====================================================

    if usuario.id_facultad != facultad_id:
        raise HTTPException(
            status_code=403,
            detail=(
                "El usuario no pertenece a la "
                "facultad seleccionada."
            )
        )

    # =====================================================
    # VALIDAR SALA
    # =====================================================

    sala: Optional[Sala] = db.get(
        Sala,
        sala_id
    )

    if sala is None:
        raise HTTPException(
            status_code=404,
            detail="La sala no existe."
        )

    if sala.id_facultad != facultad_id:
        raise HTTPException(
            status_code=403,
            detail=(
                "La sala seleccionada no pertenece "
                "a la facultad seleccionada."
            )
        )

    # Regla R5:
    # una sala deshabilitada no admite reservas.

    if sala.estado != EstadoSala.HABILITADA.value:
        raise HTTPException(
            status_code=422,
            detail=(
                f"La sala {sala.nombre} "
                "esta deshabilitada."
            )
        )

    # =====================================================
    # VALIDAR HORARIO
    # =====================================================

    _validar_horario(
        esquema.hora_inicio,
        esquema.hora_fin
    )

    # =====================================================
    # VALIDAR SOLAPAMIENTO
    # =====================================================

    if crud_reserva.existe_solapamiento(
        db,
        sala.id_sala,
        esquema.fecha,
        esquema.hora_inicio,
        esquema.hora_fin
    ):
        raise HTTPException(
            status_code=409,
            detail=(
                "La sala ya tiene una reserva vigente "
                "en ese horario."
            )
        )

    # =====================================================
    # CREAR RESERVA
    # =====================================================

    reserva = Reserva(
        id_sala=sala.id_sala,
        id_usuario=usuario.id_usuario,
        fecha=esquema.fecha,
        hora_inicio=esquema.hora_inicio,
        hora_fin=esquema.hora_fin,
        estado=EstadoReserva.ACTIVA.value,
    )

    db.add(reserva)
    db.flush()

    # =====================================================
    # AUDITORÍA
    # =====================================================

    crud_auditoria.registrar(
        db,
        entidad=EntidadAuditoria.RESERVA.value,
        entidad_id=reserva.id_reserva,
        accion=AccionAuditoria.CREAR.value,
        id_usuario=usuario.id_usuario,
        descripcion={
            "despues": _payload(reserva)
        },
    )

    db.commit()
    db.refresh(reserva)

    return reserva


def cancelar_reserva(
    db: Session,
    reserva_id: int,
    usuario: Optional[Usuario]
) -> Reserva:

    reserva = db.get(
        Reserva,
        reserva_id
    )

    if reserva is None:
        raise HTTPException(
            status_code=404,
            detail="La reserva no existe."
        )

    # Regla R3:
    # si el docente se identifico,
    # solo cancela sus propias reservas.

    if (
        usuario is not None
        and usuario.rol == Rol.DOCENTE.value
        and reserva.id_usuario != usuario.id_usuario
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                "Un docente solo puede cancelar "
                "sus propias reservas."
            )
        )

    if reserva.estado == EstadoReserva.CANCELADA.value:
        raise HTTPException(
            status_code=400,
            detail="La reserva ya esta cancelada."
        )

    anterior = _payload(reserva)

    reserva.estado = EstadoReserva.CANCELADA.value

    crud_auditoria.registrar(
        db,
        entidad=EntidadAuditoria.RESERVA.value,
        entidad_id=reserva.id_reserva,
        accion=AccionAuditoria.CANCELAR.value,
        id_usuario=(
            usuario.id_usuario
            if usuario
            else None
        ),
        descripcion={
            "antes": anterior,
            "despues": _payload(reserva)
        },
    )

    db.commit()
    db.refresh(reserva)

    return reserva


def ajustar_reserva(
    db: Session,
    reserva_id: int,
    esquema: ReservaAjuste,
    usuario: Optional[Usuario]
) -> Reserva:

    # Regla R4:
    # si se identifico, solo la secretaria puede ajustar.

    if (
        usuario is not None
        and usuario.rol != Rol.SECRETARIA.value
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                "Solo la secretaria puede ajustar "
                "o corregir reservas."
            )
        )

    reserva = db.get(
        Reserva,
        reserva_id
    )

    if reserva is None:
        raise HTTPException(
            status_code=404,
            detail="La reserva no existe."
        )

    if reserva.estado == EstadoReserva.CANCELADA.value:
        raise HTTPException(
            status_code=400,
            detail=(
                "No se puede ajustar "
                "una reserva cancelada."
            )
        )

    # =====================================================
    # DETERMINAR LA SALA
    # =====================================================

    sala_actual = db.get(
        Sala,
        reserva.id_sala
    )

    if sala_actual is None:
        raise HTTPException(
            status_code=404,
            detail="La sala actual no existe."
        )

    nueva_sala_id = reserva.id_sala

    if esquema.salaId is not None:

        nueva_sala = db.get(
            Sala,
            esquema.salaId
        )

        if nueva_sala is None:
            raise HTTPException(
                status_code=404,
                detail="La nueva sala no existe."
            )

        if (
            nueva_sala.id_facultad
            != sala_actual.id_facultad
        ):
            raise HTTPException(
                status_code=403,
                detail=(
                    "La nueva sala debe pertenecer "
                    "a la misma facultad de la reserva."
                )
            )

        if (
            nueva_sala.estado
            != EstadoSala.HABILITADA.value
        ):
            raise HTTPException(
                status_code=422,
                detail=(
                    f"La sala {nueva_sala.nombre} "
                    "esta deshabilitada."
                )
            )

        nueva_sala_id = nueva_sala.id_sala

    # =====================================================
    # VALIDAR HORARIO
    # =====================================================

    _validar_horario(
        esquema.hora_inicio,
        esquema.hora_fin
    )

    # =====================================================
    # VALIDAR DISPONIBILIDAD
    # =====================================================

    if crud_reserva.existe_solapamiento(
        db,
        nueva_sala_id,
        esquema.fecha,
        esquema.hora_inicio,
        esquema.hora_fin,
        excluir_id=reserva.id_reserva
    ):
        raise HTTPException(
            status_code=409,
            detail=(
                "El ajuste genera solapamiento "
                "con otra reserva vigente."
            )
        )

    # =====================================================
    # GUARDAR CAMBIOS
    # =====================================================

    anterior = _payload(reserva)

    reserva.id_sala = nueva_sala_id
    reserva.fecha = esquema.fecha
    reserva.hora_inicio = esquema.hora_inicio
    reserva.hora_fin = esquema.hora_fin
    reserva.estado = EstadoReserva.AJUSTADA.value

    # =====================================================
    # AUDITORÍA
    # =====================================================

    crud_auditoria.registrar(
        db,
        entidad=EntidadAuditoria.RESERVA.value,
        entidad_id=reserva.id_reserva,
        accion=AccionAuditoria.AJUSTAR.value,
        id_usuario=(
            usuario.id_usuario
            if usuario
            else None
        ),
        descripcion={
            "motivo_ajuste": esquema.motivo,
            "antes": anterior,
            "despues": _payload(reserva)
        },
    )

    db.commit()
    db.refresh(reserva)

    return reserva