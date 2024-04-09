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



------------------------------------------------------------------------------------------------------------------
-- ENCUESTADOS 

-- Register:Creacion de funcion para agregar el encuestado en la tabla usuario y luego con dicho id generado 
-- 		    se agrega en la tabla encuestado

CREATE OR REPLACE FUNCTION public.register_respondents(
 	nombre_encuestado VARCHAR (255),
	pass_encuestado VARCHAR(255),
 	edad_encuestado INT)
	RETURNS VOID
	LANGUAGE 'plpgsql'
	
AS $BODY$
DECLARE
 	id_nuevo INT;
BEGIN 
 	--Inserta el usuario a la tabla de usuario
 	INSERT INTO usuario(nombre,pass,idRol) VALUES (nombre_encuestado,pass_encuestado, 3) -- idRol = 3 por ser encuestado
 	RETURNING id INTO id_nuevo;
 	--Inserta el usuario en la tabla de encuestado con el id que se genero
 	INSERT INTO encuestado(id_usuario, nombre, pass, edad) VALUES (id_nuevo, nombre_encuestado, pass_encuestado, edad_encuestado);
END;
$BODY$;

------------------------------------------------------------------------------------------------------------------
-- Update: Creacion de funcion para actualizar/modificar el encuestado en las dos tablas

CREATE OR REPLACE FUNCTION public.update_respondents(
    id_encuestado INT,
    nuevo_nombre VARCHAR(255),
	nuevo_pass VARCHAR(255),
    nueva_edad INT)
	RETURNS integer
	LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    id_user INT;
	encuestado_existe BOOLEAN;
BEGIN
    SELECT EXISTS (SELECT 1 FROM Encuestado WHERE id = id_encuestado) INTO encuestado_existe;
    IF encuestado_existe THEN
    	-- Obtiene el id_usuario correspondiente al id_encuestado
		SELECT id_usuario INTO id_user
		FROM Encuestado
		WHERE id = id_encuestado;

    	-- Actualiza el nombre y la edad del encuestado en la tabla encuestado
		UPDATE Encuestado
		SET nombre = nuevo_nombre, edad = nueva_edad, pass = nuevo_pass
		WHERE id = id_encuestado;
		
		-- Actualiza el nombre y la contraseña del usuario 
		UPDATE usuario
		SET nombre = nuevo_nombre, pass = nuevo_pass
		WHERE id = id_user;

        RETURN 1; --  Se actualizo el encuestado y su usuario asociado
    ELSE
        RETURN 0; -- El encuestado no existe
    END IF;
END;
$BODY$;

------------------------------------------------------------------------------------------------------------------
-- delete: Creacion de funcion para eliminar el encuestado en las dos tablas

CREATE OR REPLACE FUNCTION public.delete_respondents(
    id_encuestado INT
)
RETURNS integer
LANGUAGE 'plpgsql'
AS $BODY$
DECLARE
    id_usuario INT;
    encuestado_existe BOOLEAN;
BEGIN
    -- Verifica si el encuestado existe
    SELECT EXISTS (SELECT 1 FROM Encuestado WHERE id = id_encuestado) INTO encuestado_existe;
    
    IF encuestado_existe THEN
        -- Obtiene el id_usuario correspondiente al id_encuestado
        SELECT id_usuario INTO id_usuario
        FROM Encuestado
        WHERE id = id_encuestado;

        -- Elimina el encuestado de la tabla Encuestado
        DELETE FROM Encuestado WHERE id = id_encuestado;

        -- Elimina el usuario de la tabla usuario
        DELETE FROM usuario WHERE id = id_usuario;

        RETURN 1; --  Se elimino el encuestado y su usuario asociado
    ELSE
        RETURN 0; -- El encuestado no existe
    END IF;
END;
$BODY$;
