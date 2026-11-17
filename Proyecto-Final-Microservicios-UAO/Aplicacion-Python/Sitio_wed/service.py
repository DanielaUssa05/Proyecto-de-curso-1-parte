import os
from pathlib import Path
from importlib import import_module
from time import monotonic
from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

if "DB_PASSWORD_FILE" in os.environ:
    password = Path(os.environ["DB_PASSWORD_FILE"]).read_text().strip()
    os.environ["DATABASE_URL"] = f"mysql+pymysql://reservas:{password}@db/reservas_salas"
from app.db.database import engine
from sqlalchemy import text
from mapreduce import report

role = os.environ["SERVICE"]
resources = {"catalogo": ["facultades", "salas"], "usuarios": ["usuarios"],
             "reservas": ["reservas"], "auditoria": ["auditoria"], "analitica": []}
app = FastAPI(title=role)
for resource in resources[role]:
    router = import_module(f"app.api.v1.{resource}").router
    app.include_router(router, prefix=f"/api/v1/{resource}")

requests = Counter("reservas_http", "Solicitudes por servicio y estado", ["servicio", "estado"])
duration = Histogram("reservas_duracion_segundos", "Tiempo de respuesta", ["servicio"])


@app.middleware("http")
async def measure(request, call_next):
    if request.url.path in ("/health", "/metrics"):
        return await call_next(request)
    start = monotonic()
    status = 500
    try:
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        requests.labels(role, str(status)).inc()
        duration.labels(role).observe(monotonic() - start)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), headers={"Content-Type": CONTENT_TYPE_LATEST})


@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1 FROM facultad LIMIT 1"))
    return {"servicio": role, "replica": os.getenv("HOSTNAME")}


if role == "analitica":
    @app.get("/api/v1/reportes/ocupacion")
    def occupancy():
        query = """SELECT s.id_facultad, r.id_sala, TIME_TO_SEC(r.hora_inicio) DIV 60,
                   TIME_TO_SEC(r.hora_fin) DIV 60 FROM reserva r JOIN sala s USING(id_sala)
                   WHERE r.estado IN ('Activa','Ajustada') ORDER BY r.id_reserva"""
        with engine.connect() as conn:
            rows = [tuple(row) for row in conn.execute(text(query))]
        return report(rows)
