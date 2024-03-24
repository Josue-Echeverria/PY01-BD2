-- \c db_tarea;

-- FUNCION PARA CREAR TAREAS

-- FUNCTION: public.create_task(character varying, text, date, integer, integer)

-- DROP FUNCTION IF EXISTS public.create_task(character varying, text, date, integer, integer);

-- CREATE OR REPLACE FUNCTION public.create_task(
-- 	inname character varying,
-- 	indescription text,
-- 	indue_date date,
-- 	inidestado integer,
-- 	inidusuario integer)
--     RETURNS integer
--     LANGUAGE 'plpgsql'
--     COST 100
--     VOLATILE PARALLEL UNSAFE
-- AS $BODY$

-- DECLARE usuario_existe BOOLEAN;
-- BEGIN
-- SELECT EXISTS ( SELECT 1 FROM usuario WHERE id = inidusuario) INTO usuario_existe;

-- IF usuario_existe THEN	
-- 	INSERT INTO tasks 
-- 		(name
-- 		, description
-- 		, due_date
-- 		, Idestado
-- 		, Idusuario)
-- 		VALUES
-- 		(Inname
-- 		, Indescription
-- 		, Indue_date
-- 		, InIdestado
-- 		, InIdusuario);
-- 	RETURN 1;
-- ELSE
-- 	RETURN 5001;
-- END IF;
-- END;
-- $BODY$;
