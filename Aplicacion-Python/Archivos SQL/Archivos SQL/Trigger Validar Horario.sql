DELIMITER $$

CREATE TRIGGER validar_horario
BEFORE INSERT ON reserva
FOR EACH ROW
BEGIN

    IF NEW.hora_inicio < '07:00:00' OR NEW.hora_fin > '21:30:00' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Horario fuera del permitido';
    END IF;

END$$

DELIMITER ;