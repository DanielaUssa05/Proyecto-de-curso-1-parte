from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_usuario_opcional
from app.core.constants import AccionAuditoria, EntidadAuditoria, EstadoSala
from app.crud import auditoria as crud_auditoria
from app.crud import sala as crud_sala
from app.models import Usuario
from app.schemas.sala import (RecursoCreate, RecursoOut, SalaConRecursosOut, SalaCreate,
                              SalaEstadoUpdate, SalaOut, SalaUpdate)

router = APIRouter()


@router.get("", response_model=List[SalaOut])
def listar_salas(facultadId: Optional[int] = None, estado: Optional[str] = None,
                 db: Session = Depends(get_db)):
    return crud_sala.get_multi(db, facultad_id=facultadId, estado=estado)


@router.get("/{sala_id}", response_model=SalaConRecursosOut)
def obtener_sala(sala_id: int, db: Session = Depends(get_db)):
    sala = crud_sala.get(db, sala_id)
    if sala is None:
        raise HTTPException(status_code=404, detail="La sala no existe.")
    recursos = crud_sala.listar_recursos(db, sala_id)
    return SalaConRecursosOut.model_validate(sala).model_copy(update={"recursos": recursos})


@router.post("", response_model=SalaOut, status_code=201)
def crear_sala(esquema: SalaCreate, db: Session = Depends(get_db)):
    if crud_sala.get_by_codigo(db, esquema.codigo):
        raise HTTPException(status_code=409, detail="Ya existe una sala con ese codigo.")
    return crud_sala.create(db, esquema)


@router.put("/{sala_id}", response_model=SalaOut)
def actualizar_sala(sala_id: int, esquema: SalaUpdate, db: Session = Depends(get_db)):
    sala = crud_sala.get(db, sala_id)
    if sala is None:
        raise HTTPException(status_code=404, detail="La sala no existe.")
    return crud_sala.update(db, sala, esquema)


@router.patch("/{sala_id}/estado", response_model=SalaOut)
def cambiar_estado_sala(sala_id: int, esquema: SalaEstadoUpdate,
                        db: Session = Depends(get_db),
                        usuario: Optional[Usuario] = Depends(get_usuario_opcional)):
    sala = crud_sala.get(db, sala_id)
    if sala is None:
        raise HTTPException(status_code=404, detail="La sala no existe.")
    accion = (AccionAuditoria.HABILITAR if esquema.estado == EstadoSala.HABILITADA
              else AccionAuditoria.DESHABILITAR)
    crud_auditoria.registrar(
        db, entidad=EntidadAuditoria.SALA.value, entidad_id=sala.id_sala,
        accion=accion.value, id_usuario=usuario.id_usuario if usuario else None,
        descripcion={"sala": sala.id_sala, "estado_anterior": sala.estado,
                     "estado_nuevo": esquema.estado.value},
    )
    sala.estado = esquema.estado.value
    db.commit()
    db.refresh(sala)
    return sala


@router.get("/{sala_id}/recursos", response_model=List[RecursoOut])
def listar_recursos(sala_id: int, db: Session = Depends(get_db)):
    return crud_sala.listar_recursos(db, sala_id)


@router.post("/{sala_id}/recursos", response_model=RecursoOut, status_code=201)
def agregar_recurso(sala_id: int, esquema: RecursoCreate, db: Session = Depends(get_db)):
    sala = crud_sala.get(db, sala_id)
    if sala is None:
        raise HTTPException(status_code=404, detail="La sala no existe.")
    return crud_sala.crear_recurso(db, sala_id, esquema)