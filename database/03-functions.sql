CREATE OR REPLACE FUNCTION public.login(
	inusername character varying,
	inuserpass character varying)
    RETURNS usuario
    LANGUAGE 'plpgsql'
AS $BODY$


DECLARE 
	my_row usuario%ROWTYPE;
BEGIN
    SELECT * INTO my_row FROM usuario WHERE (nombre = inusername AND pass = inuserpass); -- Fetch the row


	RETURN my_row;

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