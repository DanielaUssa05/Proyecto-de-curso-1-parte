from datetime import date, time
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.constants import EstadoReserva


# =========================================================
# HORARIOS PERMITIDOS PARA RESERVAS
# =========================================================

HORAS_INICIO = [
    "07:00",
    "07:30",
    "08:00",
    "08:30",
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "12:00",
    "12:30",
    "13:00",
    "13:30",
    "14:00",
    "14:30",
    "15:00",
    "15:30",
    "16:00",
    "16:30",
    "17:00",
    "17:30",
    "18:00",
    "18:30",
    "19:00",
    "19:30",
    "20:00",
    "20:30",
    "21:00",
]

HORAS_FIN = [
    "07:30",
    "08:00",
    "08:30",
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "12:00",
    "12:30",
    "13:00",
    "13:30",
    "14:00",
    "14:30",
    "15:00",
    "15:30",
    "16:00",
    "16:30",
    "17:00",
    "17:30",
    "18:00",
    "18:30",
    "19:00",
    "19:30",
    "20:00",
    "20:30",
    "21:00",
    "21:30",
]


# =========================================================
# VALIDACIÓN DE HORARIOS
# =========================================================

def validar_hora(
    hora: time,
    horas_permitidas: list[str]
) -> time:

    hora_formateada = hora.strftime("%H:%M")

    if hora_formateada not in horas_permitidas:
        raise ValueError(
            "La hora debe estar dentro de las franjas disponibles "
            "de 30 minutos."
        )

    return hora


# =========================================================
# CREAR RESERVA
# =========================================================

class ReservaCreate(BaseModel):
    fecha: date

    hora_inicio: time = Field(
        description="Hora de inicio de la reserva.",
        json_schema_extra={
            "enum": HORAS_INICIO
        }
    )

    hora_fin: time = Field(
        description="Hora de finalización de la reserva.",
        json_schema_extra={
            "enum": HORAS_FIN
        }
    )

    @field_validator("hora_inicio")
    @classmethod
    def validar_hora_inicio(
        cls,
        value: time
    ) -> time:
        return validar_hora(
            value,
            HORAS_INICIO
        )

    @field_validator("hora_fin")
    @classmethod
    def validar_hora_fin(
        cls,
        value: time
    ) -> time:
        return validar_hora(
            value,
            HORAS_FIN
        )


# =========================================================
# AJUSTAR RESERVA
# =========================================================

class ReservaAjuste(BaseModel):
    salaId: Optional[int] = Field(
        default=None,
        description=(
            "Nueva sala. Si no se envía, se conserva la sala actual."
        )
    )

    fecha: date

    hora_inicio: time = Field(
        description="Nueva hora de inicio de la reserva.",
        json_schema_extra={
            "enum": HORAS_INICIO
        }
    )

    hora_fin: time = Field(
        description="Nueva hora de finalización de la reserva.",
        json_schema_extra={
            "enum": HORAS_FIN
        }
    )

    motivo: str = Field(
        min_length=5,
        max_length=300,
        description="Motivo por el cual se ajusta la reserva."
    )

    @field_validator("hora_inicio")
    @classmethod
    def validar_hora_inicio(
        cls,
        value: time
    ) -> time:
        return validar_hora(
            value,
            HORAS_INICIO
        )

    @field_validator("hora_fin")
    @classmethod
    def validar_hora_fin(
        cls,
        value: time
    ) -> time:
        return validar_hora(
            value,
            HORAS_FIN
        )


# =========================================================
# SALIDA DE RESERVA
# =========================================================

class ReservaOut(BaseModel):
    id_reserva: int
    id_sala: int
    id_usuario: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: EstadoReserva

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================================================
# FRANJA OCUPADA
# =========================================================

class FranjaOcupada(BaseModel):
    hora_inicio: time
    hora_fin: time
    estado: EstadoReserva


# =========================================================
# FRANJA DISPONIBLE
# =========================================================

class FranjaDisponible(BaseModel):
    hora_inicio: time
    hora_fin: time


# =========================================================
# DISPONIBILIDAD DE UNA SALA
# =========================================================

class DisponibilidadSalaOut(BaseModel):
    id_sala: int
    codigo: int
    nombre: str
    estado: str
    ocupadas: List[FranjaOcupada]
    disponibles: List[FranjaDisponible]


# =========================================================
# DISPONIBILIDAD POR FACULTAD
# =========================================================

class DisponibilidadOut(BaseModel):
    id_facultad: int
    fecha: date
    salas: List[DisponibilidadSalaOut]