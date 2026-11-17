
import csv
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from configuracion import (
    SALAS,
    USUARIOS,
    FACULTADES,
    ESTADOS,
    MESES
)

# ==========================================
# CONFIGURACION
# ==========================================

BASE = Path(__file__).parent
ARCHIVO_ENTRADA = BASE / "datos" / "reservas_simuladas.csv"
CARPETA_SALIDA = BASE / "resultados"

CARPETA_SALIDA.mkdir(exist_ok=True)

reservas = []


# ==========================================
# CARGAR DATOS
# ==========================================

def cargar_datos():

    with open(
        ARCHIVO_ENTRADA,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:

        lector = csv.DictReader(archivo)

        for fila in lector:

            fila["id_sala"] = int(fila["id_sala"])
            fila["id_usuario"] = int(fila["id_usuario"])

            reservas.append(fila)

    print(f"Reservas cargadas: {len(reservas)}")


# ==========================================
# UTILIDADES
# ==========================================

def guardar_csv(nombre, encabezados, filas):

    ruta = CARPETA_SALIDA / nombre

    with open(
        ruta,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:

        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        escritor.writerows(filas)

    print(f"Archivo generado: {ruta}")


def porcentaje(cantidad, total):

    if total == 0:
        return 0

    return round(cantidad / total * 100, 2)


# ==========================================
# ANALISIS POR ESTADO
# ==========================================

def analizar_estados():

    conteo = Counter(
        r["estado"] for r in reservas
    )

    filas = []

    for estado in ESTADOS:

        cantidad = conteo[estado]

        filas.append([
            estado,
            cantidad,
            porcentaje(cantidad, len(reservas))
        ])

    guardar_csv(
        "analisis_estados.csv",
        ["estado", "cantidad", "porcentaje"],
        filas
    )

    print("\nDISTRIBUCION POR ESTADO")

    for fila in filas:
        print(
            f"{fila[0]}: {fila[1]} "
            f"({fila[2]}%)"
        )


# ==========================================
# ANALISIS MENSUAL
# ==========================================

def analizar_meses():

    conteo = Counter(
        datetime.strptime(
            r["fecha"], "%Y-%m-%d"
        ).month
        for r in reservas
    )

    filas = []

    for mes, nombre in MESES.items():

        filas.append([
            nombre,
            conteo[mes],
            porcentaje(conteo[mes], len(reservas))
        ])

    guardar_csv(
        "analisis_mensual.csv",
        ["mes", "cantidad", "porcentaje"],
        filas
    )

    print("\nDISTRIBUCION MENSUAL")

    for fila in filas:
        print(f"{fila[0]}: {fila[1]}")


# ==========================================
# ANALISIS POR SALA
# ==========================================

def analizar_salas():

    conteo = Counter(
        r["id_sala"] for r in reservas
    )

    filas = []

    for id_sala, sala in SALAS.items():

        cantidad = conteo[id_sala]

        filas.append([
            id_sala,
            sala["nombre"],
            cantidad,
            porcentaje(cantidad, len(reservas))
        ])

    guardar_csv(
        "analisis_salas.csv",
        ["id_sala", "nombre_sala", "reservas", "porcentaje"],
        filas
    )

    print("\nRESERVAS POR SALA")

    for fila in filas:
        print(
            f"{fila[1]}: {fila[2]} "
            f"({fila[3]}%)"
        )


# ==========================================
# ANALISIS POR FACULTAD
# ==========================================

def analizar_facultades():

    conteo = Counter()

    for r in reservas:

        id_facultad = USUARIOS[
            r["id_usuario"]
        ]["facultad"]

        conteo[id_facultad] += 1

    filas = []

    for id_facultad, nombre in FACULTADES.items():

        cantidad = conteo[id_facultad]

        filas.append([
            nombre,
            cantidad,
            porcentaje(cantidad, len(reservas))
        ])

    guardar_csv(
        "analisis_facultades.csv",
        ["facultad", "reservas", "porcentaje"],
        filas
    )

    print("\nRESERVAS POR FACULTAD")

    for fila in filas:
        print(
            f"{fila[0]}: {fila[1]} "
            f"({fila[2]}%)"
        )


# ==========================================
# ANALISIS POR HORARIO
# ==========================================

def analizar_horarios():

    conteo = Counter()

    for r in reservas:

        hora = datetime.strptime(
            r["hora_inicio"], "%H:%M:%S"
        ).hour

        conteo[hora] += 1

    filas = []

    for hora in sorted(conteo):

        filas.append([
            f"{hora:02d}:00",
            conteo[hora]
        ])

    guardar_csv(
        "analisis_horarios.csv",
        ["hora_inicio", "reservas"],
        filas
    )

    print("\nDEMANDA POR HORA DE INICIO")

    for fila in filas:
        print(f"{fila[0]}: {fila[1]} reservas")


# ==========================================
# ANALISIS DE DURACION
# ==========================================

def analizar_duraciones():

    conteo = Counter()

    for r in reservas:

        inicio = datetime.strptime(
            r["hora_inicio"], "%H:%M:%S"
        )

        fin = datetime.strptime(
            r["hora_fin"], "%H:%M:%S"
        )

        duracion = int(
            (fin - inicio).total_seconds() / 60
        )

        conteo[duracion] += 1

    filas = []

    for duracion in sorted(conteo):

        filas.append([
            duracion,
            conteo[duracion],
            porcentaje(conteo[duracion], len(reservas))
        ])

    guardar_csv(
        "analisis_duraciones.csv",
        ["duracion_minutos", "cantidad", "porcentaje"],
        filas
    )

    print("\nDURACION DE RESERVAS")

    for fila in filas:
        print(
            f"{fila[0]} minutos: {fila[1]}"
        )


# ==========================================
# INDICADORES GENERALES
# ==========================================

def generar_indicadores():

    total = len(reservas)

    activas = sum(
        1 for r in reservas
        if r["estado"] == "Activa"
    )

    canceladas = sum(
        1 for r in reservas
        if r["estado"] == "Cancelada"
    )

    ajustadas = sum(
        1 for r in reservas
        if r["estado"] == "Ajustada"
    )

    minutos_programados = 0

    for r in reservas:

        inicio = datetime.strptime(
            r["hora_inicio"], "%H:%M:%S"
        )

        fin = datetime.strptime(
            r["hora_fin"], "%H:%M:%S"
        )

        if r["estado"] != "Cancelada":

            minutos_programados += int(
                (fin - inicio).total_seconds() / 60
            )

    indicadores = [
        ["Total de reservas", total],
        ["Reservas activas", activas],
        ["Reservas ajustadas", ajustadas],
        ["Reservas canceladas", canceladas],
        [
            "Porcentaje de cancelacion",
            porcentaje(canceladas, total)
        ],
        [
            "Minutos programados no cancelados",
            minutos_programados
        ],
        [
            "Horas programadas no canceladas",
            round(minutos_programados / 60, 2)
        ]
    ]

    guardar_csv(
        "indicadores_generales.csv",
        ["indicador", "valor"],
        indicadores
    )

    print("\nINDICADORES GENERALES")

    for indicador, valor in indicadores:
        print(f"{indicador}: {valor}")


# ==========================================
# EJECUCION PRINCIPAL
# ==========================================

def main():

    print("=" * 50)
    print("ANALISIS ESTADISTICO DE RESERVAS UAO")
    print("=" * 50)

    cargar_datos()

    analizar_estados()
    analizar_meses()
    analizar_salas()
    analizar_facultades()
    analizar_horarios()
    analizar_duraciones()
    generar_indicadores()

    print("\nANALISIS FINALIZADO")
    print("Resultados guardados en la carpeta resultados.")
    print("No se realizaron modificaciones en MySQL.")

    print("=" * 50)


if __name__ == "__main__":
    main()
