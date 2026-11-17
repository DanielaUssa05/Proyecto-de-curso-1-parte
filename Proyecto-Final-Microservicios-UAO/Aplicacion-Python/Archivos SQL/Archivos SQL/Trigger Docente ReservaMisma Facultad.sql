DELIMITER $$

CREATE TRIGGER validar_docente_facultad
BEFORE INSERT ON reserva
FOR EACH ROW
BEGIN
    DECLARE facultad_usuario INT;
    DECLARE facultad_sala INT;
    DECLARE rol_usuario VARCHAR(20);

    SELECT id_facultad, rol INTO facultad_usuario, rol_usuario
    FROM usuario
    WHERE id_usuario = NEW.id_usuario;

    SELECT id_facultad INTO facultad_sala
    FROM sala
    WHERE id_sala = NEW.id_sala;

    IF rol_usuario = 'Docente' AND facultad_usuario <> facultad_sala THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El docente solo puede reservar salas de su facultad';
    END IF;
END$$

DELIMITER ;