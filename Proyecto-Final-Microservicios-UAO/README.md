# Sistema Web de Reservas de Salas de Reuniones por Facultad

Proyecto de la asignatura **REDES E INFRAESTRUCTURA DE DATOS** · Programa de Datos e Inteligencia Artificial · Universidad Autónoma de Occidente (UAO).

## Descripción

Sistema web que permite consultar la disponibilidad y gestionar las reservas de las salas de reuniones asignadas a cada facultad.

Las salas se utilizan para actividades administrativas y académicas de coordinación (reuniones docentes, comités curriculares, acreditación y planeación), y **no para dictar clases**.

El proyecto implementa una arquitectura basada en microservicios, con herramientas de contenedorización, monitoreo y visualización de métricas.

Adicionalmente, incorpora un módulo de simulación de reservas que permite generar datos ficticios, analizarlos estadísticamente y visualizar sus resultados mediante Prometheus y Grafana, sin modificar los registros originales de MySQL.

## Funcionalidades

- **Facultades y salas:** catálogo de facultades y salas, con nombre o código, estado (habilitada/deshabilitada), observaciones y recursos.
- **Usuarios:** creación, actualización y activación/inactivación de usuarios con rol Docente o Secretaria, asociados a una facultad.
- **Reservas:** consulta de disponibilidad por facultad y fecha, creación, cancelación y ajuste de reservas.
- **Auditoría:** historial de cancelaciones, ajustes de reservas y cambios de estado de las salas, con información del usuario y fecha de la operación.
- **Analítica:** procesamiento de información de reservas mediante MapReduce.
- **Simulación:** generación de reservas ficticias para analizar el comportamiento de la ocupación de las salas.
- **Monitoreo:** recopilación de métricas de infraestructura y de los datos simulados mediante Prometheus.
- **Visualización:** dashboard en Grafana con indicadores de infraestructura y estadísticas de las reservas.

## Reglas de negocio

- Las reservas solo se permiten en el horario institucional: **7:00 a. m. a 9:30 p. m.**
- No se permite el solapamiento de horarios en una misma sala.
- Los docentes reservan salas de su facultad y cancelan sus propias reservas.
- Las secretarias registran, ajustan o corrigen reservas en situaciones excepcionales.
- Toda acción relevante queda registrada para auditoría.

## Tecnologías

| Capa | Tecnología |
|---|---|
| Base de datos | MySQL |
| Backend | Python, FastAPI, SQLAlchemy |
| Frontend | HTML, CSS y JavaScript |
| Microservicios | Python y FastAPI |
| Contenedores | Docker |
| Orquestación | Docker Swarm |
| Balanceo y gateway | Nginx |
| Procesamiento distribuido | MapReduce |
| Monitoreo | Prometheus |
| Visualización | Grafana |
| Exportador de métricas | Python y prometheus-client |
| Análisis y gráficas | Python y Matplotlib |

## Arquitectura del proyecto

El sistema está organizado mediante microservicios independientes:

- **Catálogo:** gestión de facultades y salas.
- **Usuarios:** administración de usuarios.
- **Reservas:** gestión de las reservas.
- **Auditoría:** registro de operaciones.
- **Analítica:** procesamiento y generación de indicadores.

La infraestructura utiliza Docker Swarm para administrar los servicios y Nginx como gateway de acceso.

Prometheus recopila métricas de los microservicios y del exportador de reservas simuladas. Grafana utiliza estas métricas para presentar información mediante paneles de visualización.

## Simulación de reservas

Se desarrolló un módulo en Python para generar datos ficticios de reservas universitarias.

### Características de la simulación

- Total: **300 reservas simuladas**.
- Periodo: agosto, septiembre y octubre de 2026.
- 100 reservas por mes.
- 5 salas habilitadas.
- 6 usuarios activos.
- Horarios de simulación: 8:00 a. m. a 6:00 p. m.
- Duraciones: 60, 90 y 120 minutos.

### Distribución de estados

| Estado | Cantidad |
|---|---:|
| Activas | 225 |
| Ajustadas | 45 |
| Canceladas | 30 |
| **Total** | **300** |

### Validación de los datos

Se implementó un programa independiente para verificar:

- Fechas y días hábiles.
- Correspondencia entre usuarios, salas y facultades.
- Horarios y duraciones.
- Estados de las reservas.
- Ausencia de solapamientos de horarios.
- Integridad de los registros generados.

La validación independiente obtuvo **0 errores en los 300 registros**.

### Archivos generados

- `reservas_simuladas.csv`: registros de las reservas.
- `resumen_simulacion.csv`: resumen de la simulación.
- `insertar_reservas_simuladas.sql`: script SQL generado como archivo, no ejecutado.

**Importante:** los datos de simulación son ficticios y se mantienen en archivos independientes. No se insertaron en MySQL ni se modificaron los registros originales de la base de datos.

## Análisis estadístico

Se desarrolló un módulo de análisis que procesa el archivo CSV y genera indicadores sobre:

- Reservas por estado.
- Reservas por mes.
- Reservas por sala.
- Reservas por facultad.
- Demanda por hora de inicio.
- Reservas por duración.
- Indicadores generales.

También se generaron seis gráficas mediante Matplotlib para facilitar la interpretación de los resultados.

### Resultados principales

| Indicador | Resultado |
|---|---:|
| Total de reservas | 300 |
| Reservas activas | 225 |
| Reservas ajustadas | 45 |
| Reservas canceladas | 30 |
| Tasa de cancelación | 10 % |
| Tiempo programado no cancelado | 393,5 horas |

## Monitoreo con Prometheus y Grafana

Se implementó un exportador independiente en Python que lee el CSV de reservas simuladas y publica métricas para Prometheus.

### Métricas disponibles

- Total de reservas simuladas.
- Reservas por estado.
- Reservas por mes.
- Reservas por sala.
- Reservas por facultad.
- Reservas por hora.
- Reservas por duración.
- Última actualización de los datos.

El exportador utiliza el puerto interno **8001** y actualiza las métricas periódicamente a partir del archivo CSV.

### Dashboard de Grafana

Se configuró un dashboard llamado **Reservas universitarias**, compuesto por 11 paneles:

**Monitoreo de infraestructura:**
1. Réplicas que responden.
2. Solicitudes por segundo.
3. Respuestas con error por minuto.
4. Latencia p95 en segundos.

**Estadísticas de reservas simuladas:**
5. Total de reservas simuladas.
6. Reservas por estado.
7. Reservas por mes.
8. Reservas por sala.
9. Reservas por facultad.
10. Demanda por hora de inicio.
11. Reservas por duración.

## Estructura del proyecto

La organización general del repositorio incluye:

```text
Proyecto-Final-Microservicios-UAO/
│
├── Aplicacion-Python/
│   └── Sitio_wed/
│       ├── app/
│       ├── frontend/
│       ├── service.py
│       ├── mapreduce.py
│       └── requirements.txt
│
├── infraestructura/
│   ├── docker/
│   ├── monitor/
│   │   ├── prometheus.yml
│   │   ├── datasource.yaml
│   │   ├── provider.yaml
│   │   └── dashboard.json
│   ├── stack.yml
│   └── iniciar.ps1
│
├── simulacion/
│   ├── datos/
│   │   ├── reservas_simuladas.csv
│   │   └── resumen_simulacion.csv
│   ├── sql/
│   │   └── insertar_reservas_simuladas.sql
│   ├── resultados/
│   │   ├── graficas/
│   │   └── archivos de análisis CSV
│   ├── configuracion.py
│   ├── generar_reservas.py
│   ├── validar_reservas.py
│   ├── analizar_reservas.py
│   ├── generar_graficas.py
│   ├── exportador_metricas.py
│   └── Dockerfile
│
└── README.md
```

## Ejecución y despliegue

### Requisitos

- Python 3.11.
- Docker Desktop.
- Docker Swarm.
- MySQL.
- PowerShell (Windows).

### Despliegue de infraestructura

Desde la carpeta raíz del proyecto, se utiliza el archivo:

```powershell
.\infraestructura\stack.yml
```

Para desplegar el stack:

```powershell
docker stack deploy --resolve-image never -c .\infraestructura\stack.yml uao
```

Para consultar los servicios:

```powershell
docker stack services uao
```

### Acceso a los servicios

| Servicio | Dirección |
|---|---|
| Aplicación web | http://localhost:8088 |
| Prometheus | http://localhost:9091 |
| Objetivos de Prometheus | http://localhost:9091/targets |
| Grafana | http://localhost:3001 |

El acceso a Grafana requiere las credenciales configuradas para el proyecto.

### Generación de la simulación

Desde la carpeta raíz:

```powershell
python .\simulacion\generar_reservas.py
```

### Validación de reservas

```powershell
python .\simulacion\validar_reservas.py
```

### Análisis estadístico

```powershell
python .\simulacion\analizar_reservas.py
```

### Generación de gráficas

```powershell
python .\simulacion\generar_graficas.py
```

Estos programas trabajan con los archivos de simulación y no necesitan insertar registros en MySQL.

## Acceso por dominio

El sistema también contempla el dominio **reservas-salas.test**, configurado en el archivo `hosts` del equipo para apuntar a `127.0.0.1`.

## Consideraciones finales

El proyecto integra la gestión de reservas universitarias mediante microservicios, procesamiento distribuido, simulación de datos y monitoreo de infraestructura.

La simulación permite evaluar estadísticas de ocupación y demostrar la integración entre Python, Prometheus y Grafana sin alterar la información real almacenada en MySQL.

Los resultados estadísticos corresponden exclusivamente a datos simulados y no representan la demanda real de las salas universitarias.

