# 🚀 GUÍA DE INICIO RÁPIDO - APLICACIÓN PYTHON

Sigue estos pasos en orden para configurar la base de datos e iniciar la API en tu computadora usando **Visual Studio Code**.

---

## 🗄️ 1. CONFIGURACIÓN DE LA BASE DE DATOS (MySQL)

Antes de encender la API, debes montar la base de datos en tu MySQL local:

### Paso A: Crear las Tablas y Datos
Abre tu gestor de MySQL (Workbench, phpMyAdmin o la extensión de VS Code) y ejecuta en estricto orden estos dos archivos ubicados en la carpeta `Archivos SQL`:
1. **`Creacion DB y Tablas.sql`** (Crea la base de datos `reservas_salas` y sus estructuras).
2. **`Datos de Prueba.sql`** (Llena las tablas con información inicial para testear).

*Nota: Los scripts de Triggers son complementarios para pruebas avanzadas.*

### Paso B: Configurar la Conexión (`.env`)
Abre el archivo `.env` que está dentro de la carpeta `Sitio_wed` y ajusta tus credenciales de MySQL en la primera línea:

* **Si tu MySQL NO tiene contraseña:** Déjalo exactamente así (vacío entre los `:` y la `@`):
  ```env
  DATABASE_URL=mysql+pymysql://root:@localhost:3306/reservas_salas
  ```
* **Si tu MySQL SÍ tiene contraseña (ej. "1234"):** Agrega tu clave en el medio:
  ```env
  DATABASE_URL=mysql+pymysql://root:1234@localhost:3306/reservas_salas
  ```

Guarda el archivo (`Ctrl + S`).

---

## ⚡ 2. INICIAR LA API

Abre una **Terminal** en VS Code (Asegúrate de que sea **PowerShell**) y ejecuta los siguientes comandos:

### Paso A: Entrar a la carpeta del código
```powershell
cd "Aplicacion-Python/Sitio_wed"
```

### Paso B: Crear el entorno virtual (Solo la primera vez)
Como las librerías no vienen incluidas en la descarga, crea tu propio entorno virtual ejecutando:
```powershell
python -m venv .venv
```
*(Espera unos segundos a que la terminal termine de procesar y te deje escribir de nuevo).*

### Paso C: Activar el entorno virtual
Ahora sí, activa el entorno virtual que acabas de crear:
```powershell
.\.venv\Scripts\Activate.ps1
```
> 💡 **Nota:** Sabrás que funcionó porque aparecerá un texto verde **`(.venv)`** al inicio de la línea en tu terminal.

### Paso D: Instalar librerías (Solo la primera vez)
Instala todas las dependencias necesarias leyendo el archivo de requerimientos:
```powershell
pip install -r requirements.txt
```

### Paso E: Encender la API
Pon a correr el servidor de desarrollo:
```powershell
uvicorn app.main:app --reload
```

---
## 🎨 4. CONFIGURACIÓN E INICIO DEL FRONTEND (Interfaz Visual)

Una vez que la API (el backend) esté encendida y corriendo en su propia terminal, abre una **segunda terminal** en VS Code (dejando la anterior abierta) para encender la interfaz de usuario:

### Paso A: Entrar a la carpeta del Frontend
Desplázate a la carpeta donde están los archivos del diseño:
```powershell
cd "Aplicacion-Python/Sitio_wed/frontend_md2"
```

### Paso B: Encender el servidor del Frontend
Como es una aplicación web directa, no necesitas instalar librerías pesadas. Solo levanta el servidor nativo de Python ejecutando:
```powershell
python -m http.server 5500
```
*(Nota: Deja esta terminal abierta para que la página web no se caiga mientras la usas).*

http://127.0.0.1:5500/#/
---

## 🌐 5. ABRIR LA APLICACIÓN COMPLETA

Abre tu navegador web favorito e ingresa a la siguiente dirección para interactuar con el sistema:

👉 **[http://127.0.0.1:5500/#/](http://127.0.0.1:5500/#/)**

¡Listo! Ya puedes ver las pantallas, gestionar las reservas de salas y verificar que los datos se guarden en tu base de datos de MySQL en tiempo real.

---
