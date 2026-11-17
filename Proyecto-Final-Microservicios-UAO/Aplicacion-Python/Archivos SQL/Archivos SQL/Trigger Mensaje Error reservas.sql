-- ----------------------------------------------------------
    -- Validacion existencia de reserva 
    -- Este trigger valida que tanto la sala
    -- como el usuario existan antes de permitir crear una reserva
    -- ----------------------------------------------------------
DROP TRIGGER IF EXISTS validar_existencia_reserva_insert;            -- Primero elimino el trigger si ya existe para evitar errores al crearlo nuevamente
DELIMITER $$

CREATE TRIGGER validar_existencia_reserva_insert                     -- crea trigger
BEFORE INSERT ON reserva                                             -- valida antes de guardar datos/ON tabla
FOR EACH ROW                                                         -- indica que el trigger se ejecuta por cada registro
BEGIN                                                                -- inicia el bloque de código
    DECLARE v_sala INT;                                              -- se crean variables para realizar validaciones
    DECLARE v_usuario INT;

    -- Validar sala
    SELECT COUNT(*) INTO v_sala
    FROM sala
    WHERE id_sala = NEW.id_sala;

    IF v_sala = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: la sala no existe, no se puede crear la reserva.';
    END IF;

    -- Validar usuario
    SELECT COUNT(*) INTO v_usuario
    FROM usuario
    WHERE id_usuario = NEW.id_usuario;

    IF v_usuario = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: el usuario no existe, no se puede crear la reserva.';
    END IF;
END$$

DELIMITER ;


-- DEMOSTRACCION --

SELECT * FROM usuario;
SELECT * FROM sala;
SELECT * FROM reserva;

-- Caso Correpto
INSERT INTO reserva (id_sala, id_usuario, fecha, hora_inicio, hora_fin, estado)
VALUES (1, 1, '2026-04-15', '08:00:00', '10:00:00', 'Activa'); 

-- Caso de error sala no existe 
INSERT INTO reserva (id_sala, id_usuario, fecha, hora_inicio, hora_fin, estado)
VALUES (999, 1, '2026-04-15', '08:00:00', '10:00:00', 'Activa');

-- Caso de erros usuario no existe 
INSERT INTO reserva (id_sala, id_usuario, fecha, hora_inicio, hora_fin, estado)
VALUES (1, 999, '2026-04-15', '08:00:00', '10:00:00', 'Activa');


