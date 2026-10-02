from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.constants import EstadoUsuario
from app.crud import auditoria as crud_auditoria
from app.crud import usuario as crud_usuario
from app.schemas.usuario import UsuarioCreate, UsuarioOut, UsuarioUpdate


router = APIRouter()


# =========================================================
# LISTAR USUARIOS
# =========================================================

@router.get("", response_model=List[UsuarioOut])
def listar_usuarios(
    facultadId: Optional[int] = None,
    rol: Optional[str] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud_usuario.get_multi(
        db,
        facultad_id=facultadId,
        rol=rol,
        estado=estado,
    )


# =========================================================
# CREAR USUARIO
# =========================================================

@router.post("", response_model=UsuarioOut, status_code=201)
def crear_usuario(
    esquema: UsuarioCreate,
    db: Session = Depends(get_db),
):
    if crud_usuario.get_by_correo(
        db,
        esquema.correo_institucional,
    ):
        raise HTTPException(
            status_code=409,
            detail="Ya existe un usuario con ese correo.",
        )

    return crud_usuario.create(db, esquema)


# =========================================================
# ACTUALIZAR USUARIO
# =========================================================

@router.put("/{usuario_id}", response_model=UsuarioOut)
def actualizar_usuario(
    usuario_id: int,
    esquema: UsuarioUpdate,
    db: Session = Depends(get_db),
):
    objetivo = crud_usuario.get(
        db,
        usuario_id,
    )

    if objetivo is None:
        raise HTTPException(
            status_code=404,
            detail="El usuario no existe.",
        )

    return crud_usuario.update(
        db,
        objetivo,
        esquema,
    )


# =========================================================
# DESACTIVAR USUARIO
# =========================================================

@router.patch("/{usuario_id}/inactivar")
def inactivar_usuario(
    usuario_id: int,
    usuarioId: Optional[int] = None,
    db: Session = Depends(get_db),
):
    # -----------------------------------------------------
    # 1. Buscar el usuario que se quiere desactivar
    # -----------------------------------------------------
    usuario_desactivado = crud_usuario.get(
        db,
        usuario_id,
    )

    if usuario_desactivado is None:
        raise HTTPException(
            status_code=404,
            detail="El usuario que desea desactivar no existe.",
        )

    # -----------------------------------------------------
    # 2. Verificar quién está realizando la acción
    # -----------------------------------------------------
    if usuarioId is None:
        raise HTTPException(
            status_code=400,
            detail="Debe indicar el ID del usuario que realiza la acción.",
        )

    usuario_decide = crud_usuario.get(
        db,
        usuarioId,
    )

    if usuario_decide is None:
        raise HTTPException(
            status_code=404,
            detail="El usuario que realiza la acción no existe.",
        )

    # -----------------------------------------------------
    # 3. Verificar que quien decide sea Secretaria
    # -----------------------------------------------------
    if usuario_decide.rol != "Secretaria":
        raise HTTPException(
            status_code=403,
            detail="Solo una Secretaria puede desactivar usuarios.",
        )

    # -----------------------------------------------------
    # 4. Verificar que pertenezcan a la misma facultad
    # -----------------------------------------------------
    if usuario_decide.id_facultad != usuario_desactivado.id_facultad:
        raise HTTPException(
            status_code=403,
            detail=(
                "La Secretaria solo puede desactivar usuarios "
                "de su misma facultad."
            ),
        )

    # -----------------------------------------------------
    # 5. Evitar que una Secretaria se desactive a sí misma
    # -----------------------------------------------------
    if usuario_decide.id_usuario == usuario_desactivado.id_usuario:
        raise HTTPException(
            status_code=400,
            detail="Una Secretaria no puede desactivar su propia cuenta.",
        )

    # -----------------------------------------------------
    # 6. Verificar si ya está inactivo
    # -----------------------------------------------------
    if usuario_desactivado.estado == EstadoUsuario.INACTIVO.value:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya se encuentra inactivo.",
        )

    # -----------------------------------------------------
    # 7. Guardar estado anterior
    # -----------------------------------------------------
    estado_anterior = usuario_desactivado.estado

    # -----------------------------------------------------
    # 8. Cambiar estado a Inactivo
    # -----------------------------------------------------
    usuario_desactivado.estado = EstadoUsuario.INACTIVO.value

    # -----------------------------------------------------
    # 9. Registrar la acción en auditoria
    # -----------------------------------------------------
    crud_auditoria.registrar(
        db,
        entidad="usuario",
        entidad_id=usuario_desactivado.id_usuario,
        accion="Deshabilitar",
        id_usuario=usuario_decide.id_usuario,
        descripcion={
            "accion": "Inactivar usuario",
            "usuario_que_decide": {
                "id_usuario": usuario_decide.id_usuario,
                "nombre": usuario_decide.nombre_completo,
                "rol": usuario_decide.rol,
                "id_facultad": usuario_decide.id_facultad,
            },
            "usuario_desactivado": {
                "id_usuario": usuario_desactivado.id_usuario,
                "nombre": usuario_desactivado.nombre_completo,
                "rol": usuario_desactivado.rol,
                "id_facultad": usuario_desactivado.id_facultad,
            },
            "antes": {
                "estado": estado_anterior,
            },
            "despues": {
                "estado": usuario_desactivado.estado,
            },
        },
    )

    # -----------------------------------------------------
    # 10. Guardar cambios
    # -----------------------------------------------------
    db.commit()
    db.refresh(usuario_desactivado)

    # -----------------------------------------------------
    # 11. Respuesta
    # -----------------------------------------------------
    return {
        "mensaje": (
            f"La Secretaria ID {usuario_decide.id_usuario} "
            f"({usuario_decide.nombre_completo}) desactivó al usuario "
            f"ID {usuario_desactivado.id_usuario} "
            f"({usuario_desactivado.nombre_completo})."
        ),
        "usuario_que_decide": {
            "id_usuario": usuario_decide.id_usuario,
            "nombre": usuario_decide.nombre_completo,
            "rol": usuario_decide.rol,
            "id_facultad": usuario_decide.id_facultad,
        },
        "usuario_desactivado": {
            "id_usuario": usuario_desactivado.id_usuario,
            "nombre": usuario_desactivado.nombre_completo,
            "rol": usuario_desactivado.rol,
            "id_facultad": usuario_desactivado.id_facultad,
            "estado": usuario_desactivado.estado,
        },
    }


# =========================================================
# ACTIVAR USUARIO
# =========================================================

@router.patch("/{usuario_id}/activar")
def activar_usuario(
    usuario_id: int,
    usuarioId: Optional[int] = None,
    db: Session = Depends(get_db),
):
    # -----------------------------------------------------
    # 1. Buscar el usuario que se quiere activar
    # -----------------------------------------------------
    usuario_activado = crud_usuario.get(
        db,
        usuario_id,
    )

    if usuario_activado is None:
        raise HTTPException(
            status_code=404,
            detail="El usuario que desea activar no existe.",
        )

    # -----------------------------------------------------
    # 2. Verificar quién está realizando la acción
    # -----------------------------------------------------
    if usuarioId is None:
        raise HTTPException(
            status_code=400,
            detail="Debe indicar el ID del usuario que realiza la acción.",
        )

    usuario_decide = crud_usuario.get(
        db,
        usuarioId,
    )

    if usuario_decide is None:
        raise HTTPException(
            status_code=404,
            detail="El usuario que realiza la acción no existe.",
        )

    # -----------------------------------------------------
    # 3. Verificar que quien decide sea Secretaria
    # -----------------------------------------------------
    if usuario_decide.rol != "Secretaria":
        raise HTTPException(
            status_code=403,
            detail="Solo una Secretaria puede activar usuarios.",
        )

    # -----------------------------------------------------
    # 4. Verificar que pertenezcan a la misma facultad
    # -----------------------------------------------------
    if usuario_decide.id_facultad != usuario_activado.id_facultad:
        raise HTTPException(
            status_code=403,
            detail=(
                "La Secretaria solo puede activar usuarios "
                "de su misma facultad."
            ),
        )

    # -----------------------------------------------------
    # 5. Evitar que una Secretaria se active a sí misma
    # -----------------------------------------------------
    if usuario_decide.id_usuario == usuario_activado.id_usuario:
        raise HTTPException(
            status_code=400,
            detail="Una Secretaria no puede modificar su propia cuenta.",
        )

    # -----------------------------------------------------
    # 6. Verificar si ya está activo
    # -----------------------------------------------------
    if usuario_activado.estado == EstadoUsuario.ACTIVO.value:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya se encuentra activo.",
        )

    # -----------------------------------------------------
    # 7. Guardar estado anterior
    # -----------------------------------------------------
    estado_anterior = usuario_activado.estado

    # -----------------------------------------------------
    # 8. Cambiar estado a Activo
    # -----------------------------------------------------
    usuario_activado.estado = EstadoUsuario.ACTIVO.value

    # -----------------------------------------------------
    # 9. Registrar la acción en auditoria
    # -----------------------------------------------------
    crud_auditoria.registrar(
        db,
        entidad="usuario",
        entidad_id=usuario_activado.id_usuario,
        accion="Habilitar",
        id_usuario=usuario_decide.id_usuario,
        descripcion={
            "accion": "Activar usuario",
            "usuario_que_decide": {
                "id_usuario": usuario_decide.id_usuario,
                "nombre": usuario_decide.nombre_completo,
                "rol": usuario_decide.rol,
                "id_facultad": usuario_decide.id_facultad,
            },
            "usuario_activado": {
                "id_usuario": usuario_activado.id_usuario,
                "nombre": usuario_activado.nombre_completo,
                "rol": usuario_activado.rol,
                "id_facultad": usuario_activado.id_facultad,
            },
            "antes": {
                "estado": estado_anterior,
            },
            "despues": {
                "estado": usuario_activado.estado,
            },
        },
    )

    # -----------------------------------------------------
    # 10. Guardar cambios
    # -----------------------------------------------------
    db.commit()
    db.refresh(usuario_activado)

    # -----------------------------------------------------
    # 11. Respuesta
    # -----------------------------------------------------
    return {
        "mensaje": (
            f"La Secretaria ID {usuario_decide.id_usuario} "
            f"({usuario_decide.nombre_completo}) activó al usuario "
            f"ID {usuario_activado.id_usuario} "
            f"({usuario_activado.nombre_completo})."
        ),
        "usuario_que_decide": {
            "id_usuario": usuario_decide.id_usuario,
            "nombre": usuario_decide.nombre_completo,
            "rol": usuario_decide.rol,
            "id_facultad": usuario_decide.id_facultad,
        },
        "usuario_activado": {
            "id_usuario": usuario_activado.id_usuario,
            "nombre": usuario_activado.nombre_completo,
            "rol": usuario_activado.rol,
            "id_facultad": usuario_activado.id_facultad,
            "estado": usuario_activado.estado,
        },
    }