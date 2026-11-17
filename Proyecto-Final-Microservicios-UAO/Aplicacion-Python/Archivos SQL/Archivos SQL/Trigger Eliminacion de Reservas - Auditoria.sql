-- ----------------------------------------------------------
-- Eliminación de reserva
-- Este trigger registra automáticamente un historial
-- cada vez que se elimina una reserva del sistema
-- guardando los datos anteriores en formato JSON
-- ----------------------------------------------------------
DELIMITER $$

CREATE TRIGGER auditoria_reserva_delete
BEFORE DELETE ON reserva
FOR EACH ROW
BEGIN
    INSERT INTO auditoria (
        id_usuario,
        entidad,
        fecha_y_hora,
        tipoAccion,
        descripcion
    )
    VALUES (
        OLD.id_usuario,
        'reserva',
        NOW(),
        'Eliminar',
        JSON_OBJECT(
            'antes', JSON_OBJECT(
                'id_reserva', OLD.id_reserva,
                'id_sala', OLD.id_sala,
                'fecha', OLD.fecha,
                'hora_inicio', OLD.hora_inicio,
                'hora_fin', OLD.hora_fin,
                'estado', OLD.estado
            )
        )
    );
END$$

DELIMITER ;

-- DEMOSTRACION --

SELECT * FROM reserva;

DELETE FROM reserva
WHERE id_reserva = 8;

SELECT * FROM auditoria;


-- Recrearla 
INSERT INTO reserva (id_reserva, id_sala, id_usuario, fecha, hora_inicio, hora_fin, estado)
VALUES (2, 1, 1, '2026-04-15', '10:00:00', '12:00:00', 'Activa');

