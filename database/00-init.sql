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


