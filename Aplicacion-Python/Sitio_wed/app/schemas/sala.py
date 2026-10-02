from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.core.constants import EstadoSala


class SalaCreate(BaseModel):
    id_facultad: int
    codigo: int
    nombre: str
    observaciones: Optional[str] = None


class SalaUpdate(BaseModel):
    nombre: Optional[str] = None
    observaciones: Optional[str] = None


class SalaEstadoUpdate(BaseModel):
    estado: EstadoSala


class SalaOut(BaseModel):
    id_sala: int
    id_facultad: int
    codigo: int
    nombre: str
    estado: EstadoSala
    observaciones: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class RecursoCreate(BaseModel):
    nombre_recurso: str
    descripcion: Optional[str] = None


class RecursoOut(BaseModel):
    id_recurso: int
    id_sala: int
    nombre_recurso: str
    descripcion: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class SalaConRecursosOut(SalaOut):
    recursos: List[RecursoOut] = []