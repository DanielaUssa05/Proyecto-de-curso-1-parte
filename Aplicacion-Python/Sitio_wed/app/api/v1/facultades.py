from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import facultad as crud_facultad
from app.schemas.facultad import FacultadCreate, FacultadOut

router = APIRouter()


@router.get(
    "",
    response_model=List[FacultadOut]
)
def listar_facultades(
    facultadId: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    if facultadId is not None:
        facultad = crud_facultad.get(
            db,
            facultadId
        )

        if facultad is None:
            raise HTTPException(
                status_code=404,
                detail="La facultad no existe."
            )

        return [facultad]

    return crud_facultad.get_multi(
        db,
        skip=skip,
        limit=limit
    )


@router.post(
    "",
    response_model=FacultadOut,
    status_code=201
)
def crear_facultad(
    esquema: FacultadCreate,
    db: Session = Depends(get_db),
):
    if esquema.codigo is not None:
        facultad_existente = crud_facultad.get_by_codigo(
            db,
            esquema.codigo
        )

        if facultad_existente:
            raise HTTPException(
                status_code=409,
                detail="Ya existe una facultad con ese codigo."
            )

    return crud_facultad.create(
        db,
        esquema
    )