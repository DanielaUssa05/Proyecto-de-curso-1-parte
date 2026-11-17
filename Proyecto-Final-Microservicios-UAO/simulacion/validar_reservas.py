
import csv
from collections import Counter
from datetime import date, datetime
from pathlib import Path

from configuracion import (
    ANIO,
    MESES,
    SALAS,
    USUARIOS,
    HORA_APERTURA,
    HORA_CIERRE,
    DURACIONES,
    ESTADOS,
    RESERVAS_POR_MES
)

# ==========================================
# CONFIGURACION
# ==========================================

BASE = Path(__file__).parent
ARCHIVO_CSV = BASE / "datos" / "reservas_simuladas.csv"

errores = []
advertencias = []

reservas = []


# ==========================================
# CARGAR CSV
# ==========================================

def cargar_reservas():

    if not ARCHIVO_CSV.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {ARCHIVO_CSV}"
        )

    with open(
        ARCHIVO_CSV,
        "r",
        newline="",
        encoding="utf-8-sig"
    ) as archivo:

        lector = csv.DictReader(archivo)

        columnas_esperadas = {
            "id_sala",
            "id_usuario",
            "fecha",
            "hora_inicio",
            "hora_fin",
            "estado"
        }

        if set(lector.fieldnames or []) != columnas_esperadas:
            errores.append(
                "Las columnas del CSV no coinciden con las esperadas."
            )

        for numero, fila in enumerate(lector, start=2):

            try:
                reserva = {
                    "fila": numero,
                    "id_sala": int(fila["id_sala"]),
                    "id_usuario": int(fila["id_usuario"]),
                    "fecha": date.fromisoformat(fila["fecha"]),
                    "hora_inicio": datetime.strptime(
                        fila["hora_inicio"], "%H:%M:%S"
                    ).time(),
                    "hora_fin": datetime.strptime(
                        fila["hora_fin"], "%H:%M:%S"
                    ).time(),
                    "estado": fila["estado"]
                }

                reservas.append(reserva)

            except (ValueError, TypeError, KeyError) as error:
                errores.append(
                    f"Fila {numero}: registro inválido: {error}"
                )


# ==========================================
# CONVERTIR HORAS A MINUTOS
# ==========================================

def convertir_minutos(hora):

    return hora.hour * 60 + hora.minute


# ==========================================
# VALIDAR CANTIDAD DE RESERVAS
# ==========================================

def validar_cantidad():

    if len(reservas) != 300:
        errores.append(
            f"Se esperaban 300 reservas y hay {len(reservas)}."
        )


# ==========================================
# VALIDAR FECHAS
# ==========================================

def validar_fechas():

    for r in reservas:

        fecha = r["fecha"]

        if fecha.year != ANIO:
            errores.append(
                f"Fila {r['fila']}: año incorrecto."
            )

        if fecha.month not in MESES:
            errores.append(
                f"Fila {r['fila']}: mes fuera del periodo."
            )

        if fecha.weekday() >= 5:
            errores.append(
                f"Fila {r['fila']}: reserva en fin de semana."
            )


# ==========================================
# VALIDAR SALAS Y USUARIOS
# ==========================================

def validar_salas_usuarios():

    for r in reservas:

        id_sala = r["id_sala"]
        id_usuario = r["id_usuario"]

        if id_sala not in SALAS:
            errores.append(
                f"Fila {r['fila']}: sala {id_sala} no habilitada."
            )
            continue

        if id_usuario not in USUARIOS:
            errores.append(
                f"Fila {r['fila']}: usuario {id_usuario} no válido."
            )
            continue

        sala = SALAS[id_sala]
        usuario = USUARIOS[id_usuario]

        if sala["facultad"] != usuario["facultad"]:
            errores.append(
                f"Fila {r['fila']}: facultad de sala y usuario diferente."
            )


# ==========================================
# VALIDAR HORARIOS
# ==========================================

def validar_horarios():

    for r in reservas:

        inicio = convertir_minutos(r["hora_inicio"])
        fin = convertir_minutos(r["hora_fin"])

        if inicio < HORA_APERTURA:
            errores.append(
                f"Fila {r['fila']}: inicio antes de la apertura."
            )

        if fin > HORA_CIERRE:
            errores.append(
                f"Fila {r['fila']}: fin después del cierre."
            )

        if fin <= inicio:
            errores.append(
                f"Fila {r['fila']}: hora final incorrecta."
            )

        if fin - inicio not in DURACIONES:
            errores.append(
                f"Fila {r['fila']}: duración no permitida."
            )


# ==========================================
# VALIDAR ESTADOS
# ==========================================

def validar_estados():

    conteo = Counter(r["estado"] for r in reservas)

    if conteo != Counter(ESTADOS):
        errores.append(
            f"Distribución de estados incorrecta: {dict(conteo)}"
        )


# ==========================================
# VALIDAR CANTIDAD MENSUAL
# ==========================================

def validar_meses():

    conteo = Counter(r["fecha"].month for r in reservas)

    for mes in MESES:

        if conteo[mes] != RESERVAS_POR_MES:
            errores.append(
                f"{MESES[mes]}: se esperaban "
                f"{RESERVAS_POR_MES}, hay {conteo[mes]}."
            )


# ==========================================
# VALIDAR SOLAPAMIENTOS
# ==========================================

def validar_solapamientos():

    reservas_ordenadas = sorted(
        reservas,
        key=lambda r: (
            r["fecha"],
            r["hora_inicio"]
        )
    )

    for i, a in enumerate(reservas_ordenadas):

        inicio_a = convertir_minutos(a["hora_inicio"])
        fin_a = convertir_minutos(a["hora_fin"])

        for b in reservas_ordenadas[i + 1:]:

            if b["fecha"] != a["fecha"]:
                break

            inicio_b = convertir_minutos(b["hora_inicio"])
            fin_b = convertir_minutos(b["hora_fin"])

            se_cruzan = (
                inicio_a < fin_b
                and fin_a > inicio_b
            )

            if se_cruzan:

                if a["id_sala"] == b["id_sala"]:
                    errores.append(
                        f"Solapamiento de sala: filas "
                        f"{a['fila']} y {b['fila']}."
                    )

                if a["id_usuario"] == b["id_usuario"]:
                    errores.append(
                        f"Solapamiento de usuario: filas "
                        f"{a['fila']} y {b['fila']}."
                    )


# ==========================================
# EJECUCION DE AUDITORIA
# ==========================================

def main():

    print("=" * 50)
    print("AUDITORIA INDEPENDIENTE DE RESERVAS UAO")
    print("=" * 50)

    cargar_reservas()

    if errores:
        print("\nNo se puede continuar por errores de lectura.")
    else:
        validar_cantidad()
        validar_fechas()
        validar_salas_usuarios()
        validar_horarios()
        validar_estados()
        validar_meses()
        validar_solapamientos()

    print("\nRESULTADOS DE AUDITORIA")
    print("-" * 50)
    print(f"Registros leídos: {len(reservas)}")
    print(f"Errores encontrados: {len(errores)}")

    if errores:

        print("\nDETALLE DE ERRORES:")

        for error in errores:
            print("-", error)

        print("\nRESULTADO: AUDITORIA NO SUPERADA")

    else:

        print("\nTodas las comprobaciones fueron superadas.")
        print("RESULTADO: AUDITORIA SUPERADA")

    print("=" * 50)


if __name__ == "__main__":
    main()
