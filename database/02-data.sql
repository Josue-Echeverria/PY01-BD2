\c db_encuestas;

INSERT INTO rol (nombre) VALUES 
  ('Administrador'),
  ('Creador de encuestas'),
  ('Encuestado');

INSERT INTO usuario(nombre, pass, idrol) VALUES 
	('aaa', '123', 2),
  ('bbb', 'asdf', 3),
	('ccc', 'qwerty', 1);

