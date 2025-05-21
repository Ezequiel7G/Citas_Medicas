DROP DATABASE IF EXISTS consultas_medicas;

CREATE DATABASE consultas_medicas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE consultas_medicas;

-- Tabla de roles
CREATE TABLE role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) UNIQUE
);

-- Tabla de usuarios
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) UNIQUE,
    email VARCHAR(120) UNIQUE,
    password_hash VARCHAR(256),
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES role (id)
);

-- Tabla de citas
CREATE TABLE cita (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME,
    medico_id INT,
    paciente_id INT,
    motivo TEXT,
    estado ENUM(
        'Agendada',
        'Cancelada',
        'Realizada'
    ),
    observaciones TEXT,
    FOREIGN KEY (medico_id) REFERENCES user (id),
    FOREIGN KEY (paciente_id) REFERENCES user (id)
);

-- Insertar roles básicos
INSERT INTO role (name) VALUES ('Admin'), ('Médico'), ('Paciente');

-- Insertar usuario administrador
INSERT INTO
    user (
        username,
        email,
        password_hash,
        role_id
    )
VALUES (
        'admin',
        'admin@example.com',
        'pbkdf2:sha256:600000$default_password_hash',
        1
    );

-- Insertar médicos de ejemplo
INSERT INTO
    user (
        username,
        email,
        password_hash,
        role_id
    )
VALUES (
        'dr.perez',
        'dr.perez@example.com',
        'pbkdf2:sha256:600000$default_password_hash',
        2
    ),
    (
        'dra.gonzalez',
        'dra.gonzalez@example.com',
        'pbkdf2:sha256:600000$default_password_hash',
        2
    );

-- Insertar pacientes de ejemplo
INSERT INTO
    user (
        username,
        email,
        password_hash,
        role_id
    )
VALUES (
        'paciente1',
        'paciente1@example.com',
        'pbkdf2:sha256:600000$default_password_hash',
        3
    ),
    (
        'paciente2',
        'paciente2@example.com',
        'pbkdf2:sha256:600000$default_password_hash',
        3
    );

-- Insertar citas de ejemplo
INSERT INTO
    cita (
        fecha_hora,
        medico_id,
        paciente_id,
        motivo,
        estado,
        observaciones
    )
VALUES (
        '2024-03-20 10:00:00',
        2,
        4,
        'Consulta de rutina',
        'Agendada',
        'Primera consulta del paciente'
    ),
    (
        '2024-03-21 11:00:00',
        3,
        5,
        'Revisión de resultados',
        'Agendada',
        'Seguimiento de tratamiento'
    ),
    (
        '2024-03-22 15:00:00',
        2,
        5,
        'Control médico',
        'Agendada',
        'Control de presión arterial'
    );

-- Crear índices para mejorar el rendimiento
CREATE INDEX idx_user_email ON user (email);

CREATE INDEX idx_user_username ON user (username);

CREATE INDEX idx_cita_fecha ON cita (fecha_hora);

CREATE INDEX idx_cita_estado ON cita (estado);

-- Crear usuario para la aplicación
CREATE USER IF NOT EXISTS 'app_user' @'localhost' IDENTIFIED BY 'tu_contraseña_segura';

GRANT ALL PRIVILEGES ON consultas_medicas.* TO 'app_user' @'localhost';

FLUSH PRIVILEGES;