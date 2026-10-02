from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.db.seed import init_db

app = FastAPI(
    title="API del Sistema de Reservas de Salas de Reuniones por Facultad",
    version="1.0.0",
    description="API para gestionar facultades, salas, usuarios (Docente/Secretaria), "
                "reservas con reglas de negocio y trazabilidad (auditoria).",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
def startup():
    init_db()