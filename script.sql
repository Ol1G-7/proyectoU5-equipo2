-- Tabla Estados
CREATE TABLE Estados (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    status INT NOT NULL
);

-- Insertar datos en la tabla Estados

INSERT INTO Estados (nombre, status) VALUES 
('Jalisco',1),
('Nuevo León',1),
('Puebla',1),
('Chiapas',1),
('Yucatán',1);

-- Tabla Municipios
CREATE TABLE Municipios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_estado INT NOT NULL,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    status INT NOT NULL,
    FOREIGN KEY (id_estado) REFERENCES Estados(id)
);

-- Municipios para Jalisco (id = 1)
INSERT INTO Municipios (nombre, id_estado, status) VALUES
('Guadalajara', 1, 1),
('Zapopan', 1, 1),
('Tlaquepaque', 1, 1),
('Tonalá', 1, 1),
('Puerto Vallarta', 1, 1);

-- Municipios para Nuevo León (id = 2)
INSERT INTO Municipios (nombre, id_estado, status) VALUES
('Monterrey', 2, 1),
('San Pedro Garza García', 2, 1),
('San Nicolás de los Garza', 2, 1),
('Apodaca', 2, 1),
('Santa Catarina', 2, 1),
('Guadalupe', 2, 1);

-- Municipios para Puebla (id = 3)
INSERT INTO Municipios (nombre, id_estado, status) VALUES
('Puebla', 3, 1),
('San Pedro Cholula', 3, 1),
('Atlixco', 3, 1),
('Tehuacán', 3, 1),
('Amozoc', 3, 1);

-- Municipios para Chiapas (id = 4)
INSERT INTO Municipios (nombre, id_estado, status) VALUES
('Tuxtla Gutiérrez', 4, 1),
('Tapachula', 4, 1),
('San Cristóbal de las Casas', 4, 1),
('Palenque', 4, 1),
('Comitán', 4, 1);

-- Municipios para Yucatán (id = 5)
INSERT INTO Municipios (nombre, id_estado, status) VALUES
('Mérida', 5, 1),
('Progreso', 5, 1),
('Tizimín', 5, 1),
('Valladolid', 5, 1),
('Motul', 5, 1);

-- Tabla Tipos_Usuarios
CREATE TABLE Tipos_Usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    nivel INT NOT NULL UNIQUE,
    descripcion TEXT NOT NULL,
    status INT NOT NULL
);

-- Inserts para la tabla Tipos_Usuarios
INSERT INTO Tipos_Usuarios (nombre, nivel, descripcion, status) VALUES
('Administrador del Sistema', 1, 'Gestión total del sistema, incluyendo usuarios, proyectos y reportes.', 1),
('Coordinador de Voluntariado', 2, 'Encargado de supervisar proyectos, validar horas y dar seguimiento a estudiantes.', 1),
('Encargado de Proyecto', 3, 'Responsable de registrar actividades y horas de los estudiantes en proyectos específicos.', 1),
('Estudiante Voluntario', 4, 'Puede registrarse en proyectos, visualizar su avance y registrar horas de servicio.', 1),
('Usuario Externo', 5, 'Organizaciones externas con acceso limitado para registrar eventos o validar participación.', 1);

-- Tabla Usuarios
CREATE TABLE Usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_tipo_usuario INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    telefono BIGINT NOT NULL,
    fecha_registro DATE NOT NULL,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    status INT NOT NULL,
    FOREIGN KEY (id_tipo_usuario) REFERENCES Tipos_Usuarios(id)
);

-- Inserts para la tabla Usuarios
INSERT INTO Usuarios (
    id_tipo_usuario, nombre, apellido_paterno, apellido_materno,
    correo, telefono, fecha_registro, usuario, password, status
) VALUES
(1, 'Luis', 'Ramírez', 'González', 'luis.ramirez@universidad.edu.mx', 5551234567, '2025-05-20', 'admin_luis', 'admin123', 1),
(2, 'María', 'Hernández', 'López', 'maria.hernandez@universidad.edu.mx', 5552345678, '2025-05-18', 'admin_maria', 'coordinador456', 1),
(3, 'Carlos', 'Mendoza', 'Sánchez', 'carlos.mendoza@universidad.edu.mx', 5553456789, '2025-05-15', 'admin_carlos', 'proyecto789', 1),
(4, 'Ana', 'Torres', 'Díaz', 'ana.torres@alumno.universidad.edu.mx', 5554567890, '2025-05-10', 'ana_torres', 'voluntaria001', 1),
(5, 'Oscar', 'Martínez', 'Reyes', 'oscar.martinez@ong.org.mx', 5555678901, '2025-05-05', 'oscar_ong', 'externo999', 1),
(4, 'Karla', 'Gómez', 'Ramírez', 'karla.gomez@alumno.universidad.edu.mx', 5556789012, '2025-05-12', 'karla_gomez', 'voluntaria002', 1),
(4, 'Oliver', 'Fernández', 'Morales', 'oliver.fernandez@alumno.universidad.edu.mx', 5557890123, '2025-05-13', 'oliver_fernandez', 'voluntario003', 1),
(4, 'Aislinn', 'Santos', 'Vargas', 'aislinn.santos@alumno.universidad.edu.mx', 5558901234, '2025-05-14', 'aislinn_santos', 'voluntaria004', 1),
(4, 'Iker', 'Navarro', 'Cruz', 'iker.navarro@alumno.universidad.edu.mx', 5559012345, '2025-05-15', 'iker_navarro', 'voluntario005', 1);

-- Tabla Departamentos
CREATE TABLE Departamentos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    status INT NOT NULL
);

-- Inserts para la tabla Departamentos
INSERT INTO Departamentos (nombre, status) VALUES
('Responsabilidad Social Universitaria', 1),
('Vinculación y Extensión', 1),
('Bienestar Estudiantil', 1),
('Servicios Comunitarios', 1),
('Sustentabilidad y Medio Ambiente', 1);


-- Tabla Administradores
CREATE TABLE Administradores (
    id_usuario INT PRIMARY KEY,
    id_departamento INT NOT NULL,
    status INT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id),
    FOREIGN KEY (id_departamento) REFERENCES Departamentos(id)
);

-- Inserts para la tabla Administradores
INSERT INTO Administradores (id_usuario, id_departamento, status) VALUES
(1, 1, 1), -- Luis Ramírez en Responsabilidad Social Universitaria
(2, 2, 1), -- María Hernández en Vinculación y Extensión
(3, 3, 1); -- Carlos Mendoza en Bienestar Estudiantil


-- Tabla Carreras
CREATE TABLE Carreras (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    status INT NOT NULL
);

-- Inserts para la tabla Carreras
INSERT INTO Carreras (nombre, status) VALUES
('Ingeniería en Sistemas Computacionales', 1),
('Ingeniería Mecatrónica', 1),
('Ingeniería Electrónica', 1),
('Ingeniería en Gestión Empresarial', 1),
('Ingeniería Electromecánica', 1);


-- Tabla Estudiantes
CREATE TABLE Estudiantes (
    id_usuario INT NOT NULL,
    matricula VARCHAR(20) NOT NULL UNIQUE,
    id_carrera INT NOT NULL,
    status INT NOT NULL,
    PRIMARY KEY (id_usuario),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id),
    FOREIGN KEY (id_carrera) REFERENCES Carreras(id)
);

INSERT INTO Estudiantes (id_usuario, matricula, id_carrera, status) VALUES
(4, 'ISC2025001', 1, 1), -- Ana Torres - Ingeniería en Sistemas Computacionales
(6, 'IMEC2025002', 2, 1), -- Karla Gómez - Ingeniería Mecatrónica
(7, 'IELE2025003', 3, 1), -- Oliver Fernández - Ingeniería Electrónica
(8, 'IGE2025004', 4, 1), -- Aislinn Santos - Ingeniería en Gestión Empresarial
(9, 'IECM2025005', 5, 1); -- Iker Navarro - Ingeniería Electromecánica

-- Tabla Responsables
CREATE TABLE Responsables (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    telefono BIGINT NOT NULL,
    correo VARCHAR(100) NOT NULL,
    status INT NOT NULL
);

INSERT INTO Responsables (nombre, apellido_paterno, apellido_materno, telefono, correo, status) VALUES
('Sofía', 'Ramírez', 'Gutiérrez', 1234859162, 'resp_sofia@example.com', 1),
('Jorge', 'Mendoza', 'López', 7486215439, 'resp_jorge@example.com', 1),
('Elena', 'Vargas', 'Castillo',2187402300, 'resp_elena@example.com', 1),
('Fernando', 'Pérez', 'Santos',7225984036, 'resp_fernando@example.com', 1),
('Mariana', 'Torres', 'Hernández',7296483052, 'resp_mariana@example.com', 1);

-- Tabla Colaboradores
CREATE TABLE Colaboradores (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
	apellido_materno VARCHAR(100) NOT NULL,
    organizacion VARCHAR(100) NOT NULL,
    telefono BIGINT NOT NULL,
    correo VARCHAR(100) NOT NULL,
    status INT NOT NULL
);

INSERT INTO Colaboradores (nombre, apellido_paterno, apellido_materno, organizacion, telefono, correo, status) VALUES
('Andrea', 'Mora', 'Sánchez', 'Cruz Roja', 5587654321, 'andrea.mora@example.com', 1),
('Ricardo', 'Gómez', 'Fernández', 'UNICEF', 5598765432, 'ricardo.gomez@example.com', 1),
('Lucía', 'Ruiz', 'Vargas', 'Greenpeace', 5576543210, 'lucia.ruiz@example.com', 1),
('Diego', 'Cruz', 'López', 'Save the Children', 5567890123, 'diego.cruz@example.com', 1),
('Natalia', 'Morales', 'Jiménez', 'Caritas', 5556789012, 'natalia.morales@example.com', 1);


-- Tabla Tipos_Voluntariados
CREATE TABLE Tipos_Voluntariados (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    status INT NOT NULL
);

INSERT INTO Tipos_Voluntariados (nombre, status) VALUES
('Proyecto', 1),
('Evento', 1);

-- Tabla Voluntariados
CREATE TABLE Voluntariados (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    actividades TEXT NOT NULL,
    objetivo TEXT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    descripcion TEXT NOT NULL,
    perfil TEXT NOT NULL,
    id_responsable INT NOT NULL,
    id_colaborador INT NOT NULL,
    id_tipo INT NOT NULL,
    vacantes INT NOT NULL,
    status INT NOT NULL,
    FOREIGN KEY (id_responsable) REFERENCES Responsables(id),
    FOREIGN KEY (id_colaborador) REFERENCES Colaboradores(id),
    FOREIGN KEY (id_tipo) REFERENCES Tipos_Voluntariados(id)
);

INSERT INTO Voluntariados (
    nombre, actividades, objetivo, fecha_inicio, fecha_fin, descripcion, perfil,
    id_responsable, id_colaborador, id_tipo, vacantes, status
) VALUES
('Reforestación en el Parque Central',
 'Plantación de árboles, limpieza de áreas verdes',
 'Contribuir a la recuperación ambiental del parque',
 '2025-06-01', '2025-06-10',
 'Voluntariado enfocado en actividades al aire libre para reforestar y limpiar.',
 'Interés en ecología y trabajo en equipo',
 1, 1, 1, 20, 1),

('Taller de Capacitación para Jóvenes',
 'Organización de talleres, registro de asistentes, logística',
 'Brindar capacitación en habilidades técnicas y sociales',
 '2025-07-15', '2025-07-20',
 'Evento con diversos talleres para jóvenes interesados en desarrollo personal.',
 'Capacidad organizativa y comunicación',
 2, 3, 2, 30, 1),

('Apoyo en Campaña de Salud Comunitaria',
 'Difusión, registro de pacientes, acompañamiento',
 'Mejorar la salud de la comunidad a través de campañas preventivas',
 '2025-08-05', '2025-08-15',
 'Voluntariado en colaboración con instituciones de salud para campañas.',
 'Empatía y capacidad de trabajo en salud comunitaria',
 3, 5, 2, 25, 1);

-- Tabla Voluntariados_Estudiantes
CREATE TABLE Voluntariados_Estudiantes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_estudiante INT NOT NULL,
    id_voluntariado INT NOT NULL,
    fecha_participacion DATE NULL,
    horas_aportadas INT NULL,
    estado_validacion VARCHAR(50) NULL,
    observaciones TEXT NULL,
    FOREIGN KEY (id_estudiante) REFERENCES Estudiantes(id_usuario),
    FOREIGN KEY (id_voluntariado) REFERENCES Voluntariados(id)
);

INSERT INTO Voluntariados_Estudiantes (
    id_estudiante, id_voluntariado, fecha_participacion, horas_aportadas, estado_validacion, observaciones
) VALUES
(4, 1, '2025-06-02', 5, 'Validado', 'Excelente participación en reforestación.'),
(6, 2, '2025-07-16', 8, 'Pendiente', 'Participó en organización del taller.'),
(7, 2, '2025-07-17', 6, 'Validado', 'Ayudó en logística y registro.'),
(8, 3, '2025-08-06', 4, 'Validado', 'Apoyo en difusión y acompañamiento.'),
(9, 3, '2025-08-10', 7, 'Pendiente', 'Participación activa en campaña de salud.');

-- Tabla Direcciones_Voluntariados
CREATE TABLE Direcciones_Voluntariados (
    id_voluntariado INT NOT NULL UNIQUE,
    calle VARCHAR(100) NOT NULL,
    numero INT NOT NULL,
    colonia VARCHAR(100) NOT NULL,
    cp VARCHAR(10) NOT NULL,
    id_municipio INT NOT NULL,
    referencias TEXT NOT NULL,
    PRIMARY KEY (id_voluntariado),
    FOREIGN KEY (id_voluntariado) REFERENCES Voluntariados(id),
    FOREIGN KEY (id_municipio) REFERENCES Municipios(id)
);

INSERT INTO Direcciones_Voluntariados (
    id_voluntariado, calle, numero, colonia, cp, id_municipio, referencias
) VALUES
(1, 'Av. Siempre Viva', 123, 'Jardines del Parque', '01234', 1, 'Frente al parque central'),
(2, 'Calle Reforma', 45, 'Centro', '56789', 6, 'Edificio principal de la universidad'),
(3, 'Calle Libertad', 78, 'San Miguel', '34567', 11, 'Cerca del centro de salud comunitaria');

