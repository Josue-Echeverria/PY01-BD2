\c db_encuestas;

INSERT INTO rol (nombre) VALUES 
  ('Administrador'),
  ('Creador de encuestas'),
  ('Encuestado');

INSERT INTO usuario(nombre, pass, idrol) VALUES 
	('admin', '123', 1),
  ('creador', 'asdf', 2),
	('encuestado0', 'qwerty', 3);


INSERT INTO usuario(nombre, pass, idrol) VALUES 
	('admin', '123', 1),
  ('creador', 'asdf', 2),
	('encuestado0', 'qwerty', 3),
	('encuestado1', 'qwerty', 3),
	('encuestado2', 'qwerty', 3),
	('encuestado3', 'qwerty', 3),
	('encuestado4', 'qwerty', 3),
	('encuestado5', 'qwerty', 3),
	('encuestado6', 'qwerty', 3),
	('encuestado7', 'qwerty', 3),
	('encuestado8', 'qwerty', 3),
	('encuestado9', 'qwerty', 3);

INSERT INTO Encuestado (id_usuario,nombre,pass,edad) values (3,'Josue','qwerty',20);
INSERT INTO Encuestado (id_usuario,nombre,pass,edad) values (4,'Jose','qwerty',20);
INSERT INTO Encuestado (id_usuario,nombre,pass,edad) values (5,'Juan','qwerty',28);
INSERT INTO Encuestado (id_usuario,nombre,pass,edad) values (6,'Johan','qwerty',20);
INSERT INTO Encuestado (id_usuario,nombre,pass,edad) values (7,'Jhon','qwerty',28);
INSERT INTO Encuestado (id_usuario,nombre,pass,edad) values (8,'Joshua','qwerty',20);
INSERT INTO Encuestado (id_usuario,nombre,pass,edad) values (9,'Joselyn','qwerty',20);
INSERT INTO Encuestado (id_usuario,nombre,pass,edad) values (10,'Geovanni','qwerty',20);
INSERT INTO Encuestado (id_usuario,nombre,pass,edad) values (11,'Anthony','qwerty',20);
INSERT INTO Encuestado (id_usuario,nombre,pass,edad) values (12,'Carlos','qwerty',20);