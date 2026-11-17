
import csv
import random
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

from configuracion import (
    SEMILLA,
    ANIO,
    MESES,
    RESERVAS_POR_MES,
    RESERVAS_POR_SALA_MES,
    HORA_APERTURA,
    HORA_CIERRE,
    DURACIONES,
    SALAS,
    USUARIOS,
    ESTADOS
)

# ==========================================
# CONFIGURACION GENERAL
# ==========================================

random.seed(SEMILLA)

BASE = Path(__file__).parent
CARPETA_DATOS = BASE / "datos"
CARPETA_SQL = BASE / "sql"

CARPETA_DATOS.mkdir(exist_ok=True)
CARPETA_SQL.mkdir(exist_ok=True)

COLUMNAS = [
    "id_sala",
    "id_usuario",
    "fecha",
    "hora_inicio",
    "hora_fin",
    "estado"
]

reservas = []
ocupacion_salas = Counter()


# ==========================================
# FUNCIONES DE HORARIO
# ==========================================

def minutos_a_hora(minutos):
    horas = minutos // 60
    minutos_restantes = minutos % 60

    return f"{horas:02d}:{minutos_restantes:02d}:00"


def fechas_habiles(mes):
    fechas = []
    dia = date(ANIO, mes, 1)

    while dia.month == mes:
        if dia.weekday() < 5:
            fechas.append(dia)

        dia += timedelta(days=1)

    return fechas


def hay_solapamiento(id_sala, id_usuario, fecha, inicio, fin):
    fecha_texto = fecha.isoformat()

    for reserva in reservas:

        # Comparar fechas en el mismo formato: texto ISO
        if reserva["fecha"] != fecha_texto:
            continue

        se_cruzan = (
            inicio < reserva["_fin"]
            and fin > reserva["_inicio"]
        )

        if se_cruzan:
            misma_sala = reserva["id_sala"] == id_sala
            mismo_usuario = reserva["id_usuario"] == id_usuario

            if misma_sala or mismo_usuario:
                return True

    return False


# ==========================================
# GENERACION DE RESERVAS
# ==========================================

def generar_mes(mes):
    fechas = fechas_habiles(mes)

    for id_sala, sala in SALAS.items():

        usuarios_validos = [
            id_usuario
            for id_usuario, usuario in USUARIOS.items()
            if usuario["facultad"] == sala["facultad"]
        ]

        if not usuarios_validos:
            raise ValueError(
                f"La sala {id_sala} no tiene usuarios disponibles."
            )

        generadas = 0
        intentos = 0
        max_intentos = 50000

        while generadas < RESERVAS_POR_SALA_MES:

            intentos += 1

            if intentos > max_intentos:
                raise RuntimeError(
                    f"No se pudieron generar suficientes reservas "
                    f"para la sala {id_sala} en el mes {mes}."
                )

            fecha = random.choice(fechas)
            duracion = random.choice(DURACIONES)

            ultimo_inicio = HORA_CIERRE - duracion

            inicio = random.randrange(
                HORA_APERTURA,
                ultimo_inicio + 1,
                30
            )

            fin = inicio + duracion

            id_usuario = random.choice(usuarios_validos)

            if hay_solapamiento(
                id_sala,
                id_usuario,
                fecha,
                inicio,
                fin
            ):
                continue

            reservas.append({
                "id_sala": id_sala,
                "id_usuario": id_usuario,
                "fecha": fecha.isoformat(),
                "hora_inicio": minutos_a_hora(inicio),
                "hora_fin": minutos_a_hora(fin),
                "estado": "",
                "_inicio": inicio,
                "_fin": fin
            })

            generadas += 1

        ocupacion_salas[(mes, id_sala)] = generadas


# ==========================================
# ASIGNACION DE ESTADOS
# ==========================================

def asignar_estados():

    estados = []

    for estado, cantidad in ESTADOS.items():
        estados.extend([estado] * cantidad)

    if len(estados) != len(reservas):
        raise ValueError(
            "La cantidad de estados no coincide con las reservas."
        )

    random.shuffle(estados)

    for reserva, estado in zip(reservas, estados):
        reserva["estado"] = estado


# ==========================================
# VALIDACION DE RESERVAS
# ==========================================

def validar():

    assert len(reservas) == sum(ESTADOS.values())

    conteo_estados = Counter(
        r["estado"] for r in reservas
    )

    assert conteo_estados == Counter(ESTADOS)

    # Validar fechas, facultades y horarios

    for reserva in reservas:

        fecha = date.fromisoformat(reserva["fecha"])

        assert fecha.year == ANIO
        assert fecha.month in MESES
        assert fecha.weekday() < 5

        sala = SALAS[reserva["id_sala"]]
        usuario = USUARIOS[reserva["id_usuario"]]

        assert sala["facultad"] == usuario["facultad"]

        inicio = reserva["_inicio"]
        fin = reserva["_fin"]

        assert inicio >= HORA_APERTURA
        assert fin <= HORA_CIERRE
        assert fin - inicio in DURACIONES

    # Validar que no existan solapamientos

    for i, a in enumerate(reservas):

        for b in reservas[i + 1:]:

            if a["fecha"] != b["fecha"]:
                continue

            se_cruzan = (
                a["_inicio"] < b["_fin"]
                and a["_fin"] > b["_inicio"]
            )

            if se_cruzan:

                if (
                    a["id_sala"] == b["id_sala"]
                    or a["id_usuario"] == b["id_usuario"]
                ):
                    raise ValueError(
                        "SOLAPAMIENTO DETECTADO:\n"
                        f"Fecha: {a['fecha']}\n"
                        f"Reserva A: sala {a['id_sala']}, "
                        f"usuario {a['id_usuario']}, "
                        f"{a['hora_inicio']} - {a['hora_fin']}\n"
                        f"Reserva B: sala {b['id_sala']}, "
                        f"usuario {b['id_usuario']}, "
                        f"{b['hora_inicio']} - {b['hora_fin']}"
                    )

    # Validar cantidades mensuales y por sala

    for mes in MESES:

        cantidad_mes = sum(
            1 for r in reservas
            if date.fromisoformat(r["fecha"]).month == mes
        )

        assert cantidad_mes == RESERVAS_POR_MES

        for id_sala in SALAS:

            assert ocupacion_salas[(mes, id_sala)] == (
                RESERVAS_POR_SALA_MES
            )

    print("Todas las validaciones fueron superadas.")


# ==========================================
# EXPORTAR CSV
# ==========================================

def exportar_csv():

    ruta = CARPETA_DATOS / "reservas_simuladas.csv"

    with open(
        ruta,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:

        escritor = csv.DictWriter(
            archivo,
            fieldnames=COLUMNAS
        )

        escritor.writeheader()

        for reserva in reservas:

            escritor.writerow({
                columna: reserva[columna]
                for columna in COLUMNAS
            })

    print(f"CSV generado: {ruta}")


# ==========================================
# EXPORTAR RESUMEN
# ==========================================

def exportar_resumen():

    ruta = CARPETA_DATOS / "resumen_simulacion.csv"

    with open(
        ruta,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:

        escritor = csv.writer(archivo)

        escritor.writerow([
            "mes",
            "id_sala",
            "nombre_sala",
            "cantidad_reservas"
        ])

        for mes, nombre_mes in MESES.items():

            for id_sala, sala in SALAS.items():

                escritor.writerow([
                    nombre_mes,
                    id_sala,
                    sala["nombre"],
                    ocupacion_salas[(mes, id_sala)]
                ])

    print(f"Resumen generado: {ruta}")


# ==========================================
# EXPORTAR SQL
# NO EJECUTAR EN MYSQL
# ==========================================

def exportar_sql():

    ruta = CARPETA_SQL / "insertar_reservas_simuladas.sql"

    with open(ruta, "w", encoding="utf-8") as archivo:

        archivo.write("-- Reservas simuladas UAO\n")
        archivo.write("-- Generadas automaticamente\n")
        archivo.write("-- Archivo para revision previa\n")
        archivo.write("-- No ejecutar sin autorizacion\n\n")

        archivo.write(
            "INSERT INTO reserva "
            "(id_sala, id_usuario, fecha, hora_inicio, hora_fin, estado)\n"
            "VALUES\n"
        )

        valores = []

        for reserva in reservas:

            valores.append(
                f"({reserva['id_sala']}, "
                f"{reserva['id_usuario']}, "
                f"'{reserva['fecha']}', "
                f"'{reserva['hora_inicio']}', "
                f"'{reserva['hora_fin']}', "
                f"'{reserva['estado']}')"
            )

        archivo.write(",\n".join(valores))
        archivo.write(";\n")

    print(f"SQL generado: {ruta}")


# ==========================================
# EJECUCION PRINCIPAL
# ==========================================

def main():

    print("Iniciando simulacion de reservas UAO...")

    for mes in MESES:

        print(f"Generando reservas de {MESES[mes]}...")

        generar_mes(mes)

    asignar_estados()

    validar()

    exportar_csv()
    exportar_resumen()
    exportar_sql()

    conteo_final = Counter(
        r["estado"] for r in reservas
    )

    print("\nSIMULACION FINALIZADA")
    print(f"Total de reservas: {len(reservas)}")
    print(f"Estados: {dict(conteo_final)}")

    print(
        "No se realizaron conexiones "
        "ni inserciones en MySQL."
    )


if __name__ == "__main__":
    main()
