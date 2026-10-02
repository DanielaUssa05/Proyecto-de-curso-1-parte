DELIMITER $$

DROP TRIGGER IF EXISTS trg_after_update_sala$$

CREATE TRIGGER trg_after_update_sala
AFTER UPDATE ON sala
FOR EACH ROW
BEGIN
    IF OLD.estado <> NEW.estado THEN
        INSERT INTO auditoria (
            id_usuario,
            entidad,
            fecha_y_hora,
            tipoAccion,
            descripcion
        ) VALUES (
            NULL,
            'sala',
            NOW(),
            IF(NEW.estado = 'Habilitada', 'Habilitar', 'Deshabilitar'),
            JSON_OBJECT(
                'sala', NEW.id_sala,
                'estado_anterior', OLD.estado,
                'estado_nuevo', NEW.estado
            )
        );
    END IF;
END$$

DELIMITER ;