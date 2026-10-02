# Sistema Web de Reservas de Salas de Reuniones por Facultad

Proyecto de la asignatura **REDES E INFRAESTRUCTURA** · Programa de Datos e Inteligencia Artificial · Universidad Autónoma de Occidente (UAO).

## Descripción

Sistema web que permite consultar la disponibilidad y gestionar las reservas de las salas de reuniones asignadas a cada facultad. Las salas se usan para actividades administrativas y académicas de coordinación (reuniones docentes, comités curriculares, acreditación, planeación) y **no para dictar clases**.

## Funcionalidades

- **Facultades y salas:** catálogo de facultades y de salas, con nombre o código, estado (habilitada/deshabilitada), observaciones y recursos (proyector, mesas, etc.).
- **Usuarios:** creación, actualización y activación/inactivación de usuarios con rol **Docente** o **Secretaria**, asociados a una facultad.
- **Reservas:** consulta de disponibilidad por facultad y fecha, creación, cancelación y ajuste de reservas (estados: activa, cancelada, ajustada).
- **Auditoría:** historial de cancelaciones, ajustes de reservas y cambios de estado de las salas, con quién lo hizo y cuándo, y filtros por entidad, acción, usuario y fechas.

## Reglas de negocio

- Las reservas solo se permiten en el horario institucional: **7:00 a. m. a 9:30 p. m.**
- No se permite solapamiento de horarios en una misma sala.
- Los **docentes** reservan salas de su facultad y cancelan sus propias reservas.
- Las **secretarias** registran, ajustan o corrigen reservas en situaciones excepcionales.
- Toda acción relevante queda registrada para auditoría.

## Tecnologías

| Capa | Tecnología |
|---|---|
| Base de datos | MySQL |
| Backend | Python, FastAPI, SQLAlchemy (async) |
| Frontend | HTML, CSS y JavaScript (sin dependencias ni build) |

## Estructura del repositorio

```
├── app/          Backend FastAPI (api, crud, models, schemas, services, db)
├── frontend/     Interfaz web
├── requirements.txt
└── README.md
```

## Cómo ejecutarlo

### 1. Base de datos
Crea la base de datos en MySQL con el script SQL del proyecto y configura los datos de conexión en un archivo `.env` en la raíz.

### 2. Backend
```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```
La API queda en `http://127.0.0.1:8000` y su documentación interactiva en `http://127.0.0.1:8000/docs`.

### 3. Frontend
En otra terminal:
```bash
cd frontend
python -m http.server 5173
```
Abre `http://localhost:5173` e ingresa con el correo institucional de un usuario registrado.

> No abras `index.html` con doble clic: los módulos de JavaScript requieren un servidor.

## Acceso por dominio

El sistema se consulta mediante el dominio **reservas-salas.test** (configurado en el archivo `hosts` del equipo, apuntando a `127.0.0.1`).
