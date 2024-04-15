\c db_encuestas;

ALTER TABLE usuario
ADD CONSTRAINT fk_rol
FOREIGN KEY (Idrol)
REFERENCES rol(id);
