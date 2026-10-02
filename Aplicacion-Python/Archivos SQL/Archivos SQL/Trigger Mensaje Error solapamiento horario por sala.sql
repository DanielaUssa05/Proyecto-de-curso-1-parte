-- ----------------------------------------------------------
--  solapamiento de reservas
-- Este trigger evita que una sala sea reservada
-- en un horario que ya esté ocupado por otra reserva activa
-- ----------------------------------------------------------
DELIMITER $$
 
CREATE TRIGGER validar_solapamiento_reserva
BEFORE INSERT ON reserva
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM reserva
        WHERE id_sala     = NEW.id_sala
          AND fecha        = NEW.fecha
          AND estado       = 'Activa'
          AND hora_inicio  < NEW.hora_fin
          AND hora_fin     > NEW.hora_inicio
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'ERROR: La sala ya tiene una reserva activa en ese horario. Por favor elige otro horario o sala.';
    END IF;
    
END$$

-- DEMOSTRACION --
-- Ver recervas existentes
SELECT * FROM reserva WHERE id_sala = 2;

INSERT INTO reserva (id_sala, id_usuario, fecha, hora_inicio, hora_fin, estado)
VALUES (2, 1, '2026-04-20', '12:00:00', '14:00:00', 'Activa');

INSERT INTO reserva (id_sala, id_usuario, fecha, hora_inicio, hora_fin, estado)
VALUES (2, 1, '2026-04-20', '13:00:00', '15:00:00', 'Activa');