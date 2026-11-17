-- PROBAR UNO POR UNO.

-- Este comando revisa toda la info registrada en auditoria
select * from auditoria;

-- Este comando actualiza la reserva a cancelada para probar Trigger de Actualizacion de Reservas.
-- NOTA. Recordar tener datos ya registrados en las tablas (Ver el archivo 'Datos de Prueba')  ('Activa', 'Cancelada', 'Ajustada'),
UPDATE reserva
SET estado = 'Cancelada'
WHERE id_reserva = 1;

select * from reserva;

-- Este comando elimina la reserva para probar Trigger de Eliminacion de Reservas.
-- NOTA. Recordar tener datos ya registrados en las tablas (Ver el archivo 'Datos de Prueba')

DELETE FROM reserva
WHERE id_reserva = 1;

select * from reserva;

INSERT INTO reserva (id_sala, id_usuario, fecha, hora_inicio, hora_fin, estado)
VALUES 
(1, 1, '2026-04-15', '08:00:00', '10:00:00', 'Activa');

-- Veo todos lo
SHOW TRIGGERS; 