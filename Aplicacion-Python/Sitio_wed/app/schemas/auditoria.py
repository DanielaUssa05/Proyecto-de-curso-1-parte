from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict


class AuditoriaOut(BaseModel):
    id_auditoria: int

    # Usuario que realizó la acción
    id_usuario: Optional[int]

    # Entidad afectada:
    # usuario / reserva / sala
    entidad: str

    # Fecha y hora de la acción
    fecha_y_hora: Optional[datetime]

    # Tipo de acción:
    # Habilitar / Deshabilitar / Actualizar / Eliminar
    tipoAccion: str

    # Información adicional
    descripcion: Optional[Dict[str, Any]]

    model_config = ConfigDict(
        from_attributes=True
    )