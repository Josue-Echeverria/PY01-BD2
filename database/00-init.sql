CREATE DATABASE db_encuestas;

\c db_encuestas;

CREATE TABLE usuario (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  pass VARCHAR(255) NOT NULL,      
  idRol INT NOT NULL
);

CREATE TABLE rol (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL
);

CREATE TABLE Encuestado (
    id SERIAL PRIMARY KEY, 
    id_usuario INT,
    nombre VARCHAR(255) NOT NULL,
    pass VARCHAR(255) NOT NULL,
    edad INT,
    CONSTRAINT FK_idUsuario FOREIGN KEY (id_usuario)
    REFERENCES usuario(id)
);


-- \c db_tarea;

  
-- CREATE TABLE estado(
--   id SERIAL PRIMARY KEY,
--   name VARCHAR(255) NOT NULL
-- );


-- CREATE TABLE tasks (
--   id SERIAL PRIMARY KEY,
--   name VARCHAR(255) NOT NULL,
--   description TEXT NOT NULL,
--   due_date DATE NOT NULL,
--   Idestado INT NOT NULL,
--   Idusuario INT NOT NULL
-- );
