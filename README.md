# PY01 DockerRestAPI

# Sistema de encuestas

Este proyecto se implementara un sistema de encuestas backend que utilizara Docker,Docker-Compose, MongoDB, PostgreSQL, Redis y RestAPI. Este sistema permitirá a los usuarios crear, publicar y gestionar encuestas con diferentes tipos de preguntas, así como registrar y administrar listas de encuestados.

Para las demostraciones de funcionamiento en los endpoints se utilizara la aplicacion Postman, ya que esta facilita el trabajo para crear request.

## Características

- Autenticación de usuarios.
- Manejo de permisos

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

Como enviar el token con postman: 
<img src="token_auth.png"/>


