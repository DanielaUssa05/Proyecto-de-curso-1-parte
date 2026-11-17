# Guion de 15 minutos
| Tiempo | Qué mostrar y decir |
|---|---|
| 0–1 | Abrir el portal. “Queremos que dos docentes puedan consultar disponibilidad y reservar sin ocupar la misma sala al mismo tiempo.” |
| 1–3 | Mostrar el diagrama. Antes, todos los routers dependían de un proceso. Ahora Nginx conserva las URLs y distribuye cada petición al servicio que corresponde. Seguir una reserva desde el navegador hasta MySQL. |
| 3–5 | Mostrar stack.yml y docker stack services uao. Explicar imagen, servicio y tarea con el caso de dos tareas de reservas. El gateway también tiene dos. Mostrar el volumen de MySQL y los secretos. |
| 5–8 | Ejecutar demo.ps1. Leer el ID de la reserva y el HTTP 409 al repetir la franja. Explicar que ambas réplicas coordinan la escritura mediante el bloqueo de la sala en la misma transacción. Abrir auditoría. |
| 8–10 | Abrir /api/v1/reportes/ocupacion. Señalar dos PID, las particiones y una fila del resultado. Dos reservas de 30 y 60 minutos en una misma sala aportan dos reservas y 90 minutos, incluso si caen en particiones distintas. |
| 10–12 | Abrir Prometheus Targets y Grafana. Señalar dos destinos de reservas y explicar qué revela una respuesta 409. Generar tráfico para mostrar latencia y tasa. |
| 12–14 | Ejecutar recuperar.ps1. Comparar ID de tareas y respuestas observadas. Si alguna petición falla durante el reemplazo, mostrarlo tal como ocurrió. |
| 14–15 | Presentar los retos que el equipo haya verificado: conexión local frente al nombre interno db, concurrencia, ENUM de auditoría. Cerrar con el alcance de un nodo y una BD compartida. |

## Sustentación individual y preguntas (5 minutos adicionales)
Cada integrante completa antes del ensayo: «Me encargué de ___; el cambio está en ___; lo comprobé con ___; al fallar ___ observé ___». Elijan tareas que hayan ejecutado y que puedan repetir.

- ¿Por qué Gateway? Permite conservar la interfaz y cambiar una implementación detrás de su ruta.
- ¿Por qué usuarios y reservas pueden compartir imagen? Se despliegan y escalan por separado. Cada proceso registra las rutas que le corresponden.
- ¿Qué ocurre si dos réplicas aceptan solicitudes simultáneas? En la misma sala se serializa la comprobación de solapamiento al bloquear su fila antes de insertar. Las dos peticiones no deben quedar confirmadas.
- ¿Qué es síncrono y qué es paralelo? El cliente espera su respuesta HTTP. Durante una consulta de analítica dos procesos computan particiones al mismo tiempo y el reducer combina sus salidas.
- ¿Qué aporta MapReduce aquí? Permite demostrar partición y agregación con números verificables. Con seis filas, el coste de crear procesos puede superar el ahorro de tiempo.
- ¿Qué pasa si falla el host o MySQL? La demo de recuperación comprueba pérdida de un contenedor de reservas. El host y la base siguen siendo puntos únicos de fallo.
- ¿Se usa CQRS o una cola de eventos? El patrón implementado es API Gateway. La auditoría se escribe en la transacción y su servicio ofrece consultas. No hay broker de eventos.
