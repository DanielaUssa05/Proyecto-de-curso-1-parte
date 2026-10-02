from fastapi import APIRouter

from app.api.v1 import auditoria, facultades, reservas, salas, usuarios

api_router = APIRouter()
api_router.include_router(facultades.router, prefix="/facultades", tags=["Facultades"])
api_router.include_router(salas.router, prefix="/salas", tags=["Salas"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
api_router.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])
api_router.include_router(auditoria.router, prefix="/auditoria", tags=["Auditoria"])