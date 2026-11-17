FROM mysql:8.4
COPY ["Aplicacion-Python/Archivos SQL/Archivos SQL/Creacion DB y Tablas.sql", "/docker-entrypoint-initdb.d/01-schema.sql"]
RUN sed -i 's/^CREATE DATABASE reservas_salas;/CREATE DATABASE IF NOT EXISTS reservas_salas;/' /docker-entrypoint-initdb.d/01-schema.sql
COPY infraestructura/docker/auditoria.sql /docker-entrypoint-initdb.d/02-auditoria.sql
COPY ["Aplicacion-Python/Archivos SQL/Archivos SQL/Datos de Prueba.sql", "/docker-entrypoint-initdb.d/03-datos.sql"]
