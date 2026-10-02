DELIMITER $$

DROP TRIGGER IF EXISTS trg_validar_secretaria_facultad$$

CREATE TRIGGER trg_validar_secretaria_facultad
BEFORE INSERT ON reserva
FOR EACH ROW
BEGIN
    DECLARE v_rol VARCHAR(20);
    DECLARE v_facultad_usuario INT;
    DECLARE v_facultad_sala INT;

    -- Obtener rol y facultad del usuario
    SELECT rol, id_facultad
    INTO v_rol, v_facultad_usuario
    FROM usuario
    WHERE id_usuario = NEW.id_usuario;

    -- Obtener facultad de la sala
    SELECT id_facultad
    INTO v_facultad_sala
    FROM sala
    WHERE id_sala = NEW.id_sala;

    -- Validación SOLO para secretarias
    IF v_rol = 'Secretaria' THEN

        IF v_facultad_usuario <> v_facultad_sala THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Error: La secretaria solo puede reservar salas de su facultad';
        END IF;

    END IF;

END$$

DELIMITER ;