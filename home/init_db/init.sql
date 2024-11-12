CREATE TABLE IF NOT EXISTS usuarios (
    identificacion VARCHAR(50) PRIMARY KEY,  -- Identificación del usuario como clave primaria
    nombre VARCHAR(100) NOT NULL,            -- Nombre del usuario
    apellido VARCHAR(100) NOT NULL,          -- Apellido del usuario
    genero VARCHAR(10) CHECK (genero IN ('Mujer', 'Hombre')) NOT NULL  -- Género: Mujer o Hombre
);
