-- ----------------------------------------------------------
-- Actualización de reserva
-- Este trigger registra automáticamente un historial
-- cada vez que se actualiza una reserva en el sistema
-- guardando los datos anteriores en formato JSON
-- ----------------------------------------------------------
DELIMITER $$

CREATE TRIGGER auditoria_reserva_update
BEFORE UPDATE ON reserva
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
        'Actualizar',
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

-- DEMOSTRACCION --

SELECT * FROM reserva WHERE id_reserva = 2;

## Actualizar reserva

UPDATE reserva
SET estado = 'Activa'                -- ('Activa', 'Cancelada', 'Ajustada')
WHERE id_reserva = 2;

## Ver auditoría
SELECT * FROM auditoria;

-- Comando para consultar Json
SELECT 
JSON_UNQUOTE(JSON_EXTRACT(descripcion, '$.antes.estado')) AS estado,
JSON_UNQUOTE(JSON_EXTRACT(descripcion, '$.antes.fecha')) AS fecha, JSON_UNQUOTE(JSON_EXTRACT(descripcion, '$.antes.id_reserva')) AS id_reserva
FROM auditoria;


