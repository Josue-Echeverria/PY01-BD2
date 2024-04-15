\c db_encuestas;

INSERT INTO rol (nombre) VALUES 
  ('Administrador'),
  ('Creador de encuestas'),
  ('Encuestado');

INSERT INTO usuario(nombre, pass, idrol) VALUES 
	('admin', '123', 1),
  ('creador', 'asdf', 2),
	('encuest', 'qwerty', 3);

