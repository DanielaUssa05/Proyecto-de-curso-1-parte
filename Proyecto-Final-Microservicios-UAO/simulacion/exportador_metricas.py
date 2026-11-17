import csv
import os
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

from prometheus_client import Gauge, start_http_server


BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "datos" / "reservas_simuladas.csv"

FACULTADES = {
    1: "Ingeniería",
    2: "Ciencias",
    3: "Administración",
    4: "Derecho",
    5: "Humanidades",
}

SALAS = {
    1: {"nombre": "Sala 101", "facultad": 1},
    2: {"nombre": "Sala 102", "facultad": 1},
    3: {"nombre": "Laboratorio 1", "facultad": 2},
    5: {"nombre": "Sala Conferencias", "facultad": 3},
    6: {"nombre": "Sala Derecho 1", "facultad": 4},
}

reservas_total = Gauge(
    "reservas_simuladas_total",
    "Cantidad de reservas simuladas",
)

reservas_estado = Gauge(
    "reservas_simuladas_por_estado",
    "Reservas simuladas agrupadas por estado",
    ["estado"],
)

reservas_mes = Gauge(
    "reservas_simuladas_por_mes",
    "Reservas simuladas agrupadas por mes",
    ["mes"],
)

reservas_sala = Gauge(
    "reservas_simuladas_por_sala",
    "Reservas simuladas agrupadas por sala",
    ["sala"],
)

reservas_facultad = Gauge(
    "reservas_simuladas_por_facultad",
    "Reservas simuladas agrupadas por facultad",
    ["facultad"],
)

reservas_hora = Gauge(
    "reservas_simuladas_por_hora",
    "Reservas simuladas agrupadas por hora de inicio",
    ["hora"],
)

reservas_duracion = Gauge(
    "reservas_simuladas_por_duracion",
    "Reservas simuladas agrupadas por duración en minutos",
    ["duracion_minutos"],
)

ultima_actualizacion = Gauge(
    "reservas_simuladas_ultima_actualizacion",
    "Fecha Unix de la última lectura del CSV",
)


def cargar_metricas():
    estados = Counter()
    meses = Counter()
    salas = Counter()
    facultades = Counter()
    horas = Counter()
    duraciones = Counter()

    total = 0

    with CSV_FILE.open(
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as archivo:

        lector = csv.DictReader(archivo)

        for fila in lector:
            total += 1

            id_sala = int(fila["id_sala"])
            estado = fila["estado"]

            fecha = datetime.strptime(
                fila["fecha"], "%Y-%m-%d"
            )

            inicio = datetime.strptime(
                fila["hora_inicio"], "%H:%M:%S"
            )

            fin = datetime.strptime(
                fila["hora_fin"], "%H:%M:%S"
            )

            duracion = int(
                (fin - inicio).total_seconds() / 60
            )

            sala = SALAS[id_sala]
            facultad = FACULTADES[sala["facultad"]]

            estados[estado] += 1
            meses[fecha.strftime("%m-%B")] += 1
            salas[sala["nombre"]] += 1
            facultades[facultad] += 1
            horas[inicio.strftime("%H:00")] += 1
            duraciones[duracion] += 1

    reservas_total.set(total)

    for estado, cantidad in estados.items():
        reservas_estado.labels(estado).set(cantidad)

    for mes, cantidad in meses.items():
        reservas_mes.labels(mes).set(cantidad)

    for sala, cantidad in salas.items():
        reservas_sala.labels(sala).set(cantidad)

    for facultad, cantidad in facultades.items():
        reservas_facultad.labels(facultad).set(cantidad)

    for hora, cantidad in horas.items():
        reservas_hora.labels(hora).set(cantidad)

    for duracion, cantidad in duraciones.items():
        reservas_duracion.labels(str(duracion)).set(cantidad)

    ultima_actualizacion.set(time.time())

    print(f"CSV procesado correctamente: {total} reservas")


if __name__ == "__main__":
    puerto = int(os.getenv("EXPORTER_PORT", "8001"))

    start_http_server(puerto)

    print(f"Exportador iniciado en puerto {puerto}")

    while True:
        try:
            cargar_metricas()
        except Exception as error:
            print(f"Error leyendo CSV: {error}")

        time.sleep(30)