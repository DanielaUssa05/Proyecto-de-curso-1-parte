# Entrega de microservicios sobre el proyecto original

1. Abre la raíz del repositorio. La aplicación de siempre arranca en Aplicacion-Python/Sitio_wed con app.main:app. El frontend local usa el puerto 5173 y la API el 8000.
2. Compara app/main.py con service.py dentro de Sitio_wed. El primero agrupa las rutas, el segundo carga las correspondientes al servicio indicado por SERVICE. Ambos importan los routers originales. mapreduce.py calcula el reporte de ocupación.
3. Revisa infraestructura/docker. Las imágenes copian la aplicación, la interfaz y los SQL desde sus carpetas originales. MySQL adapta el CREATE DATABASE y las columnas de auditoría al preparar una base vacía. La inicialización con datos de prueba solo ocurre la primera vez sobre un volumen vacío.
4. Desde la raíz, abre Docker Desktop y ejecuta en PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -File .\infraestructura\iniciar.ps1
docker stack services uao
```
El despliegue usa el mismo stack uao, los mismos secretos y el volumen uao_mysql del ensayo anterior en ese Docker Desktop. Publica MySQL en 3307 y conserva la instalación Windows en 3306. Espera a que todos los servicios alcancen el número de réplicas; comprueba la reserva 7 en el portal si has usado el mismo volumen. Portal: http://localhost:8088 ; Prometheus: http://localhost:9091/targets ; Grafana: http://localhost:3001/d/reservas . El login de demostración es carlos@uni.edu; Grafana usa admin y la clave del ensayo anterior (inicial Grafana-Demo-Reservas).
5. Desde la misma raíz, ensaya con demo.ps1 y recuperar.ps1 en infraestructura. El primero crea y cancela una reserva de prueba, el segundo detiene una tarea de reservas y comprueba que se recupera. El guion, diagrama y presentación están en infraestructura/docs.
