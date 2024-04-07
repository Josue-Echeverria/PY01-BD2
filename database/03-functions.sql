\c db_encuestas;

CREATE OR REPLACE FUNCTION public.login(
	inusername character varying,
	inuserpass character varying)
    RETURNS integer
    LANGUAGE 'plpgsql'
AS $BODY$


DECLARE 
	userol integer;
BEGIN
    SELECT idrol INTO userol FROM usuario WHERE (nombre = inusername AND pass = inuserpass); -- Fetch the row

	RETURN userol;

END;
$BODY$;

------------------------------------------------------------------------------------------------------------------



CREATE OR REPLACE FUNCTION public.register(
	inusername character varying,
	inuserpass character varying,
	inuserrol integer)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$

DECLARE existe_usuario BOOLEAN;
BEGIN
SELECT EXISTS (SELECT 1 FROM usuario WHERE nombre = inusername) INTO existe_usuario;
IF existe_usuario THEN	
	RETURN 5000; --Usuario ya existe 
ELSE
    INSERT INTO usuario 
        (nombre
		, pass
		, idrol
		)
		VALUES
		(inUserName
		, inUserPass
		, inuserrol
		);
	RETURN 1;
END IF;
END;
$BODY$;


-- UPDATE user

CREATE OR REPLACE FUNCTION public.update_user(	
	inuserid integer,
	inusername character varying,
	inuserpass character varying,
	inuserrol integer)
    RETURNS integer
    LANGUAGE 'plpgsql'
AS $BODY$
DECLARE 
    usuario_existe BOOLEAN;
    old_user RECORD;
BEGIN
    SELECT EXISTS (SELECT 1 FROM usuario WHERE id = inuserid) INTO usuario_existe;

    IF usuario_existe THEN
		SELECT * INTO old_user FROM usuario WHERE id = inuserid;
		UPDATE usuario
		SET 
			nombre = COALESCE(inusername, old_user.nombre),
			pass = COALESCE(inuserpass, old_user.pass),
			idrol = COALESCE(inuserrol, old_user.idrol)
		WHERE
			id = inuserid;
	
		RETURN 1; -- Se actualizó el usuario exitosamente	
	ELSE
        RETURN 5001; -- El usuario especificado no existe
    END IF;
END;
$BODY$;