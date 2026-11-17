# Proyecto final de Microservicios — UAO

Sistema de reservas de salas universitarias.
Profesor: Heberth Martinez.

El proyecto incluye FastAPI, MySQL, API Gateway con Nginx,
Docker Swarm, Prometheus, Grafana y procesamiento paralelo con MapReduce.

## Código e instrucciones

- [Abrir el proyecto completo](./Proyecto-Final-Microservicios-UAO/)
- [Leer las instrucciones de ejecución](./Proyecto-Final-Microservicios-UAO/LEEME-ENTREGA.md)
- [Consultar la infraestructura](./Proyecto-Final-Microservicios-UAO/infraestructura/)

## Ejecutar desde PowerShell

Con Docker Desktop iniciado, entrar a la carpeta del proyecto y ejecutar:

```powershell
cd Proyecto-Final-Microservicios-UAO
powershell -ExecutionPolicy Bypass -File .\infraestructura\iniciar.ps1
docker stack services uao
