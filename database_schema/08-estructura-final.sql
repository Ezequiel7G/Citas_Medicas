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
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    rol VARCHAR(20) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de doctores
CREATE TABLE doctor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    especialidad VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);

-- Tabla de pacientes
CREATE TABLE paciente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(20),
    direccion VARCHAR(200),
    FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);

-- Tabla de citas
CREATE TABLE cita (
    id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_id INT NOT NULL,
    paciente_id INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    estado VARCHAR(20) DEFAULT 'pendiente',
    motivo TEXT,
    notas TEXT,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doctor_id) REFERENCES doctor (id) ON DELETE CASCADE,
    FOREIGN KEY (paciente_id) REFERENCES paciente (id) ON DELETE CASCADE
);

-- Insertar roles básicos
INSERT INTO role (name) VALUES ('admin'), ('doctor'), ('paciente');

-- Crear índices para mejorar el rendimiento
CREATE INDEX idx_user_email ON user (email);

CREATE INDEX idx_cita_fecha ON cita (fecha_hora);

CREATE INDEX idx_cita_estado ON cita (estado);

CREATE INDEX idx_doctor_especialidad ON doctor (especialidad);