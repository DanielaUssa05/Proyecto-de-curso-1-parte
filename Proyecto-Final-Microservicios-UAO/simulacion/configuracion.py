# ==========================================
# CONFIGURACION DE SIMULACION DE RESERVAS UAO
# ==========================================

# Semilla para reproducir los mismos resultados
SEMILLA = 20261026

# Periodo de simulacion
ANIO = 2026

MESES = {
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre"
}

# Cantidad de reservas
RESERVAS_POR_MES = 100
RESERVAS_POR_SALA_MES = 20

# Horario permitido (en minutos)
HORA_APERTURA = 8 * 60
HORA_CIERRE = 18 * 60

# Duraciones permitidas
DURACIONES = [60, 90, 120]

# ==========================================
# FACULTADES
# ==========================================

FACULTADES = {
    1: "Ingeniería",
    2: "Ciencias",
    3: "Administración",
    4: "Derecho",
    5: "Humanidades"
}

# ==========================================
# SALAS HABILITADAS
# ==========================================

SALAS = {
    1: {"facultad": 1, "nombre": "Sala 101"},
    2: {"facultad": 1, "nombre": "Sala 102"},
    3: {"facultad": 2, "nombre": "Laboratorio 1"},
    5: {"facultad": 3, "nombre": "Sala Conferencias"},
    6: {"facultad": 4, "nombre": "Sala Derecho 1"}
}

# ==========================================
# USUARIOS ACTIVOS
# ==========================================

USUARIOS = {
    1: {"facultad": 1, "nombre": "Carlos Ramirez"},
    2: {"facultad": 1, "nombre": "Ana Torres"},
    3: {"facultad": 2, "nombre": "Luis Gomez"},
    5: {"facultad": 3, "nombre": "Pedro Castillo"},
    6: {"facultad": 3, "nombre": "Laura Mendez"},
    7: {"facultad": 4, "nombre": "Miguel Rojas"}
}

# ==========================================
# ESTADOS DE LAS RESERVAS
# ==========================================

ESTADOS = {
    "Activa": 225,
    "Ajustada": 45,
    "Cancelada": 30
}

# ==========================================
# VALIDACIONES
# ==========================================

assert sum(ESTADOS.values()) == 300

for id_sala, sala in SALAS.items():
    assert any(
        usuario["facultad"] == sala["facultad"]
        for usuario in USUARIOS.values()
    ), f"La sala {id_sala} no tiene usuarios de su facultad"

print("Configuracion cargada correctamente.")
print(f"Salas habilitadas: {len(SALAS)}")
print(f"Usuarios activos: {len(USUARIOS)}")
print(f"Reservas objetivo: {sum(ESTADOS.values())}")