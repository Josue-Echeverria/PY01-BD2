# PY01 DockerRestAPI

# Sistema de encuestas

Este proyecto se implementara un sistema de encuestas backend que utilizara Docker,Docker-Compose, MongoDB, PostgreSQL, Redis y RestAPI. Este sistema permitirá a los usuarios crear, publicar y gestionar encuestas con diferentes tipos de preguntas, así como registrar y administrar listas de encuestados.

Para las demostraciones de funcionamiento en los endpoints se utilizara la aplicacion Postman, ya que esta facilita el trabajo para crear requests.

## Características

- Tokens

Los *tokens* son un conjunto de datos codificados en un *string* de caracteres. Los *tokens* nos permiten autenticar a los usuarios y manejar sus permisos de una forma segura dentro de la *app*, ya que cada vez que un usuario inicia sesión se genera un *token* el cual posee el nombre y el rol de este usuario, por lo que caundo un usuario desee realizar alguna operacion en la *app*, solo deba de enviar el *token* que se le generó cuando inicio sesion, eliminando así la necesidad del usuario de tener que introducir su nombre y contraseña cada vez que realiza una función. Para la implementación de los *tokens* se utilizará la librería llamada [flask_jwt_extended](https://flask-jwt-extended.readthedocs.io/en/stable/index.html), la cual automatiza el área de codificación y decodificación de los *tokens*, junto con *Redis* para almacenar los *jti* (json token identifier) y agilizar las consultas sobre la vigencia de los *tokens*.

Para más información conforme a esta implementación con redis: https://flask-jwt-extended.readthedocs.io/en/stable/blocklist_and_token_revoking.html#redis

Utilizando Postman, el token debe de ser enviado como *Authorization* de tipo *Bearer Token*

Como enviar el token con postman: 
<img src="token_auth.png"/>


[Link del Api](http://localhost:5002)

# Commandos 


## Construye y ejecuta el contenedor de docker
``` bash
docker-compose up --build
```


## Ejecuta el módulo de pruebas unitarias
``` bash
docker compose exec app poetry run python -m unittest test-api -v
```
# Funciones
## Registro de usuario usando postman
El cliente podra registrar un usuario en cualquier momento sin la necesidad de permisos.
 
``` bash
(POST) http://localhost:5002/auth/register
```
Formato del Body: 
``` bash
{
	"name": "nombre del usuario",
    "password": "contraseña del usuario",
	"rol": 1  
}
```
Los privilegios del usuario dependeran del rol con el que se haya creado.
Estos se dividen en:
1. Admin
2. Creador de encuestas
3. Encuestado
Por lo tanto en el body de ejemplo se estaria creando un usuario con privilegios de admin.


## Inicio de sesión usando postman
El cliente podra iniciar sesion con los credenciales de algun usuario registrado para obtener acceso segun sus privilegios.

``` bash
(POST) http://localhost:5002/auth/login
```
Formato del Body: 
``` bash
{
	"name": "nombre del usuario",
    "password": "contraseña del usuario"
}
```
Si el usuario existe, se retorna al cliente un access_token:
``` bash
{
	"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMjM0NjgwOCwianRpIjoiZDA4ZWJkMzktYzUyOC00ODEyLTk2NjYtODI2NzNkOTcyOTAxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJpZCI6MywicHJpdmlsaWdlIjoxfSwibmJmIjoxNzEyMzQ2ODA4LCJjc3JmIjoiYWUzZjI5YWEtMzllZC00M2UxLWFjZjAtNTkzMjc2OTg5NTgzIiwiZXhwIjoxNzEyMzUwNDA4fQ.ihJt2nMaI9YO0cAZpp98g0ZlZI_SbNCRC8vc_1K7VUY"
}
```

Este token se debe almacenar por parte del cliente para poder ser autenticado y poder realizar los request para los que posee privilegios.

## Cerrar sesión usando postman
Esta es una funcion la cual solo podran accesar los usuario que han iniciado sesion (Los privilegios no importan)
Por lo tanto esta funcion require el token del cliente, este se puede enviar como "Bearer" de la Autorizacion del request 

``` bash
(GET) http://localhost:5002/auth/logout
```


## Listar todos los usuarios
Para esta funcion solo podran accesar los usuarios registrados como administradores (requiere un token de administrador) y se devuelve todo los datos de los usuarios registras (id, nombre, contraseña, id del rol).


``` bash
(GET) http://localhost:5002/users
```

## Obtener usuario especifico
Muy parecida a la funcion anterior (requiere un token de administrador), la unica diferencia que devuelve la informacion del usuario con el id especificado en la direccion.

``` bash
(GET) http://localhost:5002/users/{id}
```


## Actualizar la información de un usuario
Funcion la cual permite actualizar la informacion como el nombre y contraseña. Cualquier usuario administrador tiene acceso a modificar cualquier usuario, mientras que los usuarios no administradores solo pueden modificar sus propias cuentas (requiere el token del usuario al que le corresponde el id de la direccion).
``` bash
(PUT) http://localhost:5002/users/{id}
```
La informacion actualizada del usuario debe ir en el body del request:

``` bash
{
	"name": "nombre actualizado",
    "password": "contraseña actualizada"
}
```

## Eliminar un usuario
Solo los administradores (requiere un token de administrador) podran eliminar un usuario para lo cual solo se necesitar el id correspondiente a ese usuario.
``` bash
(DELETE) http://localhost:5002/users/{id}
```

# Encuestas

## Crear encuestas

Para crear una encuesta se utiliza el siguiente endpoint:
``` bash
(POST) http://localhost:5002/surveys
```

Con el siguiente formato de body:
``` bash
{
    "description": "primera encuesta de ejemplo",
    "name": "encuesta 1",
    "id_survey": 1
}
```
Esto retornará un "_id" de confirmación

## Listar encuestas publicas
Cualquier usuario registrado puede acceder a las encuestas publicas usando:
``` bash
(GET) http://localhost:5002/surveys
```

## Listar todas las encuestas
Los administradores y creadores de encuestas podran acceder a todas las encuestas creadas con:
``` bash
(GET) http://localhost:5002/surveys/all
```

## Detalles de encuesta
Si una encuesta está publicada todos los usuarios pueden acceder a los detalles de la encuesta con su id_survey. Si no está publicada solo creadores y administradores podrán acceder. El endpoint es:
``` bash
(GET) http://localhost:5002/surveys/{id_survey}
```
y retorna la información de la encuesta:

``` bash
{
    "_id": "661ceb612506f50157ed36b1",
    "description": "primera encuesta de ejemplo",
    "id_survey": {id_survey},
    "name": "encuesta 1",
    "published": false
}
```
## Modificar encuesta
Los administradores y creadores pueden modificar el nombre y la descripción de una encuesta con:
``` bash
(PUT) http://localhost:5002/surveys/{id}
```
agregando las modificaciones en el siguiente formato:

``` bash
{
    "description": "primera encuesta de ejemplo modificada",
    "name": "encuesta 1mod"
}
```

## Publicar encuesta
Las encuestas cuando son creadas se les asigna por defecto false al atributo published. Para que un administrador o creador pueda hacer visible para todos los usuarios una encuesta se utiliza:

``` bash
(POST) http://localhost:5002/surveys/{id}/publish
```

## Ocultar encuesta
De la misma manera es posible ocultar una encuesta ya publicada con:
``` bash
(POST) http://localhost:5002/surveys/{id}/hide
```

## Eliminar encuesta
Para eliminar una encuesta con un id_survey especifico:
 ``` bash
(DELETE) http://localhost:5002/surveys/{id}
```
(Solo usuarios con privilegios)