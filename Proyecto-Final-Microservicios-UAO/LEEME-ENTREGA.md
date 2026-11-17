# Sistema de reservas universitarias
Entrega final de Microservicios · Profesor Heberth Martinez

Abre esta carpeta completa en VS Code. En Aplicacion-Python están el proyecto original, los scripts SQL, el modelo y la descripción. En infraestructura están el despliegue y los materiales de la entrega.

## Arranque en Docker Desktop desde PowerShell
Abre Docker Desktop en modo Linux y, desde esta carpeta, ejecuta:
```powershell
powershell -ExecutionPolicy Bypass -File .\infraestructura\iniciar.ps1
docker stack services uao
```
El script despliega sobre el stack uao. Con el mismo Docker Desktop, reutiliza los volúmenes y secretos existentes. En un equipo nuevo carga los datos de demostración. Verifica 2/2 en gateway y reservas, y 1/1 en los demás servicios. Portal: http://localhost:8088. El detalle de acceso, monitoreo y pruebas está en infraestructura/LEEME.md.

## Archivos de la exposición
- infraestructura/docs/arquitectura.pdf y arquitectura.dot: diagrama listo para entregar y fuente editable.
- infraestructura/docs/presentacion.pptx: presentación grupal.
- infraestructura/docs/sustentacion.md: guion de 15 minutos, demo y preguntas. Cada integrante debe completar su contribución real al preparar la exposición.
- infraestructura/demo.ps1 y recuperar.ps1: pruebas en vivo con datos del laboratorio.

El archivo .env.example sirve para ejecución local del proyecto anterior. Si eliges ese modo, cópialo como .env junto a requirements.txt y configura tus credenciales privadas. El despliegue Swarm lee los secretos creados por iniciar.ps1.
