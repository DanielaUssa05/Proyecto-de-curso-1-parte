-- CONSULTAS

-- 1. Identifica las salas que casi no se usan. (Permite detectar recursos desperdiciados y tomar decisiones como reasignar o mejorar su uso.)
SELECT
    s.nombre,
    COUNT(r.id_reserva) AS total_reservas
FROM sala s
LEFT JOIN reserva r ON r.id_sala = s.id_sala AND r.estado = 'Activa'
GROUP BY s.id_sala
HAVING COUNT(r.id_reserva) <= 1;


-- 2. Muestra cuáles secretarias realizan más reservas. (Ayuda a analizar la carga de trabajo y distribuir mejor las tareas.)
SELECT 
    u.nombre_completo,
    COUNT(r.id_reserva) AS total_reservas_gestionadas
FROM usuario u
JOIN reserva r ON r.id_usuario = u.id_usuario
WHERE u.rol = 'Secretaria'
GROUP BY u.id_usuario
ORDER BY total_reservas_gestionadas DESC;


-- 3. Mide cuánto se usan las salas en cantidad y tiempo. (Permite analizar la ocupación real y tomar decisiones de capacidad.)
SELECT 
    f.nombre AS facultad,
    s.nombre AS sala,
    COUNT(r.id_reserva) AS total_reservas,
    SUM(TIMESTAMPDIFF(HOUR, r.hora_inicio, r.hora_fin)) AS horas_usadas
FROM sala s
JOIN facultad f ON f.id_facultad = s.id_facultad
LEFT JOIN reserva r ON r.id_sala = s.id_sala AND r.estado = 'Activa'
GROUP BY f.nombre, s.nombre
ORDER BY horas_usadas DESC;


-- 4. Identifica las horas con más reservas. (Ayuda a optimizar horarios y mejorar la disponibilidad.)
SELECT 
    HOUR(hora_inicio) AS hora,
    COUNT(*) AS cantidad_reservas,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM reserva), 2) AS porcentaje
FROM reserva
GROUP BY HOUR(hora_inicio)
ORDER BY cantidad_reservas DESC;


-- 5. Salas con mayor tiempo total ocupado (Mide cuánto tiempo real se usan las salas (no solo cuántas veces).
SELECT 
    s.nombre AS sala,
    SUM(TIMESTAMPDIFF(HOUR, r.hora_inicio, r.hora_fin)) AS horas_totales
FROM sala s
JOIN reserva r ON r.id_sala = s.id_sala
WHERE r.estado = 'Activa'
GROUP BY s.id_sala
ORDER BY horas_totales DESC;


-- 6. Usuarios que más cancelan reservas
SELECT 
    u.nombre_completo,
    COUNT(r.id_reserva) AS cancelaciones
FROM usuario u
JOIN reserva r ON r.id_usuario = u.id_usuario
WHERE r.estado = 'Cancelada'
GROUP BY u.id_usuario
ORDER BY cancelaciones DESC;


-- 7. Promedio de duración de reservas por sala (Mide cuánto duran en promedio las reuniones.)
SELECT 
    s.nombre,
    AVG(TIMESTAMPDIFF(MINUTE, r.hora_inicio, r.hora_fin)) AS duracion_promedio_min
FROM sala s
JOIN reserva r ON r.id_sala = s.id_sala
WHERE r.estado = 'Activa'
GROUP BY s.id_sala;


-- 8. Usuarios que reservan pero nunca cancelan
SELECT 
    u.nombre_completo,
    COUNT(r.id_reserva) AS reservas
FROM usuario u
JOIN reserva r ON r.id_usuario = u.id_usuario
GROUP BY u.id_usuario
HAVING SUM(CASE WHEN r.estado = 'Cancelada' THEN 1 ELSE 0 END) = 0;


-- 9. Tiempo total reservado por día (Mide carga real del sistema por día.)
-- Saber días más ocupados en horas reales
-- Analizar saturación
SELECT 
    fecha,
    SUM(TIMESTAMPDIFF(HOUR, hora_inicio, hora_fin)) AS horas_totales
FROM reserva
WHERE estado = 'Activa'
GROUP BY fecha
ORDER BY horas_totales DESC;


-- 10. Facultades con mayor uso de salas (Mide qué facultad usa más el sistema.)
SELECT 
    f.nombre AS facultad,
    COUNT(r.id_reserva) AS total_reservas
FROM facultad f
JOIN sala s ON s.id_facultad = f.id_facultad
JOIN reserva r ON r.id_sala = s.id_sala
WHERE r.estado = 'Activa'
GROUP BY f.id_facultad
ORDER BY total_reservas DESC;