from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.constants import EstadoUsuario, Rol


class UsuarioCreate(BaseModel):
    id_facultad: int
    nombre_completo: str
    correo_institucional: EmailStr
    rol: Rol


class UsuarioUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    rol: Optional[Rol] = None


class UsuarioOut(BaseModel):
    id_usuario: int
    id_facultad: int
    nombre_completo: str
    correo_institucional: EmailStr
    rol: Rol
    estado: EstadoUsuario
    fecha_creacion: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)