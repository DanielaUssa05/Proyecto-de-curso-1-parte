
import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTADOS_DIR = os.path.join(BASE_DIR, "resultados")
GRAFICAS_DIR = os.path.join(RESULTADOS_DIR, "graficas")

os.makedirs(GRAFICAS_DIR, exist_ok=True)


def cargar(nombre):
    ruta = os.path.join(RESULTADOS_DIR, nombre)
    return pd.read_csv(ruta)


def guardar_grafica(nombre):
    ruta = os.path.join(GRAFICAS_DIR, nombre)
    plt.tight_layout()
    plt.savefig(ruta, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Grafica generada: {ruta}")


# 1. Reservas por estado
df = cargar("analisis_estados.csv")

plt.figure(figsize=(8, 5))
plt.bar(df.iloc[:, 0].astype(str), df.iloc[:, 1])

plt.title("Distribucion de reservas por estado")
plt.xlabel("Estado")
plt.ylabel("Cantidad de reservas")

guardar_grafica("reservas_por_estado.png")


# 2. Reservas por mes
df = cargar("analisis_mensual.csv")

plt.figure(figsize=(8, 5))
plt.bar(df.iloc[:, 0].astype(str), df.iloc[:, 1])

plt.title("Reservas por mes")
plt.xlabel("Mes")
plt.ylabel("Cantidad de reservas")

guardar_grafica("reservas_por_mes.png")


# 3. Reservas por sala
df = cargar("analisis_salas.csv")

plt.figure(figsize=(10, 6))
plt.bar(df.iloc[:, 0].astype(str), df.iloc[:, 1])

plt.title("Distribucion de reservas por sala")
plt.xlabel("Sala")
plt.ylabel("Cantidad de reservas")
plt.xticks(rotation=25, ha="right")

guardar_grafica("reservas_por_sala.png")


# 4. Reservas por facultad
df = cargar("analisis_facultades.csv")

plt.figure(figsize=(9, 5))
plt.bar(df.iloc[:, 0].astype(str), df.iloc[:, 1])

plt.title("Distribucion de reservas por facultad")
plt.xlabel("Facultad")
plt.ylabel("Cantidad de reservas")
plt.xticks(rotation=20, ha="right")

guardar_grafica("reservas_por_facultad.png")


# 5. Demanda por hora de inicio
df = cargar("analisis_horarios.csv")

plt.figure(figsize=(9, 5))
plt.plot(
    df.iloc[:, 0].astype(str),
    df.iloc[:, 1],
    marker="o"
)

plt.title("Demanda de reservas por hora de inicio")
plt.xlabel("Hora")
plt.ylabel("Cantidad de reservas")
plt.grid(True)

guardar_grafica("demanda_por_hora.png")


# 6. Duracion de las reservas
df = cargar("analisis_duraciones.csv")

plt.figure(figsize=(8, 5))
plt.bar(df.iloc[:, 0].astype(str), df.iloc[:, 1])

plt.title("Distribucion por duracion de reserva")
plt.xlabel("Duracion en minutos")
plt.ylabel("Cantidad de reservas")

guardar_grafica("reservas_por_duracion.png")


print("\nGENERACION DE GRAFICAS FINALIZADA")
print(f"Ubicacion: {GRAFICAS_DIR}")
