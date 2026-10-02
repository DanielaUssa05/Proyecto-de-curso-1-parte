from pydantic import BaseModel, ConfigDict


class FacultadCreate(BaseModel):
    id_facultad: int | None = None
    codigo: int | None = None
    nombre: str
    descripcion: str | None = None
    estado: str = "ACTIVO"


class FacultadOut(BaseModel):
    id_facultad: int
    codigo: int
    nombre: str
    descripcion: str | None
    estado: str

    model_config = ConfigDict(
        from_attributes=True
    )
