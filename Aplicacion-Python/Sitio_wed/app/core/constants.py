from enum import Enum


# Valores EXACTOS de los ENUM de tu base de datos MySQL
class Rol(str, Enum):
    DOCENTE = "Docente"
    SECRETARIA = "Secretaria"


class EstadoUsuario(str, Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"


class EstadoSala(str, Enum):
    HABILITADA = "Habilitada"
    DESHABILITADA = "Deshabilitada"


class EstadoReserva(str, Enum):
    ACTIVA = "Activa"
    CANCELADA = "Cancelada"
    AJUSTADA = "Ajustada"


class EntidadAuditoria(str, Enum):
    RESERVA = "reserva"
    SALA = "sala"


class AccionAuditoria(str, Enum):
    CREAR = "Crear"
    CANCELAR = "Cancelar"
    AJUSTAR = "Ajustar"
    ELIMINAR = "Eliminar"
    ACTUALIZAR = "Actualizar"
    HABILITAR = "Habilitar"
    DESHABILITAR = "Deshabilitar"


# Reservas que aun ocupan la sala (para validar solapamientos)
ESTADOS_RESERVA_VIGENTES = (EstadoReserva.ACTIVA.value, EstadoReserva.AJUSTADA.value)