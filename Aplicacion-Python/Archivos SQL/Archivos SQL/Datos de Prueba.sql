-- FACULTAD
INSERT INTO facultad (codigo, nombre, descripcion, estado)            -- insetar datos dentro de una tabla 
VALUES                                                                -- Valores que voy a insertar 
(101, 'Ingenieria', 'Facultad de Ingenieria', 'ACTIVO'),
(102, 'Ciencias', 'Facultad de Ciencias Basicas', 'ACTIVO'),
(103, 'Administracion', 'Facultad de Administracion', 'ACTIVO'),
(104, 'Derecho', 'Facultad de Derecho', 'ACTIVO'),
(105, 'Humanidades', 'Facultad de Humanidades','ACTIVO');

-- USUARIO
INSERT INTO usuario (id_facultad, nombre_completo, correo_institucional, rol, estado, fecha_creacion)
VALUES 
(1, 'Carlos Ramirez', 'carlos@uni.edu', 'Docente', 'Activo', NOW()),  -- NOW: Guardar automáticamente la fecha y hora en que se creó el registro
(1, 'Ana Torres', 'ana@uni.edu', 'Secretaria', 'Activo', NOW()),
(2, 'Luis Gomez', 'luis@uni.edu', 'Docente', 'Activo', NOW()),
(2, 'Sofia Herrera', 'sofia@uni.edu', 'Docente', 'Inactivo', NOW()),
(3, 'Pedro Castillo', 'pedro@uni.edu', 'Docente', 'Activo', NOW()),
(3, 'Laura Mendez', 'laura@uni.edu', 'Secretaria', 'Activo', NOW()),
(4, 'Miguel Rojas', 'miguel@uni.edu', 'Docente', 'Activo', NOW());

-- SALA
INSERT INTO sala (id_facultad, codigo, nombre, estado, observaciones)
VALUES 
(1, 201, 'Sala 101', 'Habilitada', 'Proyector disponible'),
(1, 202, 'Sala 102', 'Habilitada', 'TV disponible'),
(2, 301, 'Laboratorio 1', 'Habilitada', '20 computadores'),
(2, 302, 'Laboratorio 2', 'Deshabilitada', 'En mantenimiento'),
(3, 401, 'Sala Conferencias', 'Habilitada', 'Capacidad 50 personas'),
(4, 501, 'Sala Derecho 1', 'Habilitada', 'Videobeam instalado');

-- RECURSO
INSERT INTO recurso (id_sala, nombre_recurso, descripcion)
VALUES 
(1, 'Proyector', 'Proyector HD'),
(1, 'Tablero', 'Tablero acrilico'),
(2, 'Televisor', 'TV 50 pulgadas'),
(3, 'Computadores', '20 equipos disponibles'),
(5, 'Microfono', 'Microfono inalambrico'),
(6, 'Videobeam', 'Videobeam Full HD');

-- RESERVA
INSERT INTO reserva (id_sala, id_usuario, fecha, hora_inicio, hora_fin, estado)
VALUES 
(1, 1, '2026-04-15', '08:00:00', '10:00:00', 'Activa'),
(1, 2, '2026-04-15', '10:00:00', '12:00:00', 'Activa'),
(2, 3, '2026-04-16', '09:00:00', '11:00:00', 'Activa'),
(3, 4, '2026-04-17', '14:00:00', '16:00:00', 'Cancelada'),
(5, 5, '2026-04-18', '07:00:00', '09:00:00', 'Activa'),
(6, 7, '2026-04-19', '11:00:00', '13:00:00', 'Activa');

-- AUDITORIA
INSERT INTO auditoria (id_usuario, entidad, fecha_y_hora, tipoAccion, descripcion) 
VALUES
(1, 'reserva', NOW(), 'Actualizar', '{"detalle": "Cambio de horario"}'),
(2, 'sala', NOW(), 'Habilitar', '{"detalle": "Sala habilitada"}'),
(3, 'reserva', NOW(), 'Eliminar', '{"detalle": "Reserva cancelada"}');

SELECT * FROM facultad;                                                 -- seleccionar → todas las columnas → de la tabla 
SELECT * FROM usuario;
SELECT * FROM sala;
SELECT * FROM reserva;
SELECT * FROM reserva;
SELECT * FROM auditoria;