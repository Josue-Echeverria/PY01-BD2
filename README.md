# Ejjemplo de uso de Docker con Python/Flask

Example Project on how to develop RESTful API with Flask and Python

El código fue obtenido del siguiente repositorio: [Repositorio](https://github.com/bbachi/python-flask-restapi.git)

[Link del Api](http://127.0.0.1:5000/api/tasks)

# Commandos 

## Construye la imagen de docker

``` bash
docker build -t flask-restapi .
```

## Corre el contenedor de docker
``` bash
docker run -d -p 5000:5000 flask-restapi
```

## Verifica que el contenedor esta corriendo
``` bash
docker ps
```

## Detiene el contenedor
``` bash
docker stop <container_id>
```

## Elimina el contenedor
``` bash
docker rm <container_id>
```

## Elimina la imagen
``` bash
docker rmi flask-restapi
```

## Ejecuta un shell dentro del contenedor
``` bash
docker exec -it python-restapi /bin/sh
```