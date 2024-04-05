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