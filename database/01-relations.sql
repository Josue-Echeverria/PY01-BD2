\c db_encuestas;

ALTER TABLE usuario
ADD CONSTRAINT fk_rol
FOREIGN KEY (Idrol)
REFERENCES rol(id);

-- ALTER TABLE tasks
-- ADD CONSTRAINT fk_estado
-- FOREIGN KEY (Idestado)
-- REFERENCES estado(id);
