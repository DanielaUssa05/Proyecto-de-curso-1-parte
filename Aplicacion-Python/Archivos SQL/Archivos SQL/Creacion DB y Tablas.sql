CREATE DATABASE reservas_salas; -- creo la base completa
USE reservas_salas;             -- seleciono en donde quiero trabajar 
-- ======================
-- TABLA: facultad
-- ======================
CREATE TABLE facultad (
    id_facultad INT AUTO_INCREMENT PRIMARY KEY,
    codigo INT UNIQUE,
    nombre VARCHAR(50),
    descripcion TEXT,
    estado ENUM('ACTIVO', 'INACTIVO')
);

-- ======================
-- TABLA: usuario
-- ======================
CREATE TABLE usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    id_facultad INT,
    nombre_completo VARCHAR(50),
    correo_institucional VARCHAR(50) UNIQUE,
    rol ENUM('Docente', 'Secretaria'),
    estado ENUM('Activo', 'Inactivo'),
    fecha_creacion DATETIME,

    FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad) -- lo que indica que cada cada usuario pertenece a una facultad
);

-- ======================
-- TABLA: sala
-- ======================
CREATE TABLE sala (
    id_sala INT AUTO_INCREMENT PRIMARY KEY,
    id_facultad INT,
    codigo INT UNIQUE,
    nombre VARCHAR(50),
    estado ENUM('Habilitada', 'Deshabilitada'),
    observaciones TEXT,

    FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad)  -- lo que indica que cada sala pertenece a una facultad específica.
);

-- ======================
-- TABLA: recurso
-- ======================
CREATE TABLE recurso (
    id_recurso INT AUTO_INCREMENT PRIMARY KEY,
    id_sala INT,
    nombre_recurso VARCHAR(50),
    descripcion TEXT,

    FOREIGN KEY (id_sala) REFERENCES sala(id_sala)   -- La tabla recurso almacena los elementos disponibles que tiene cada sala
);

-- ======================
-- TABLA: reserva
-- ======================
CREATE TABLE reserva (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_sala INT,
    id_usuario INT,
    fecha DATE,
    hora_inicio TIME,
    hora_fin TIME,
    estado ENUM('Activa', 'Cancelada', 'Ajustada'),

    FOREIGN KEY (id_sala) REFERENCES sala(id_sala),         -- ya que registra las reservas realizadas. 
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) -- Relaciona un usuario con una sala en una fecha y horario específico
);

-- ======================
-- TABLA: auditoria
-- ======================
CREATE TABLE auditoria (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    entidad ENUM('reserva', 'sala'),
    fecha_y_hora DATETIME,
    tipoAccion ENUM('Eliminar', 'Actualizar', 'Habilitar', 'Deshabilitar'),
    descripcion JSON,                                         -- Se utiliza un campo JSON para almacenar detalles de los cambios

    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)   -- se utiliza para relacionar cada registro con el usuario que realizó la acción, permitiendo identificar quién hizo cada cambio en el sistema
);

