import os

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, decode_token, get_jwt
from redis.sentinel import Sentinel 
from app_service import AppService
from db import Database
from datetime import timedelta


users = Blueprint('users', __name__)


LESS_FIELDS_RES = {"error": "Not the required fields"}
NOT_SAME_USER = {"error": "The id in the request and the id of this user do not coincide"}
ERROR_INCORRECT_LOGIN = {"error": "Incorrect user or password"}  
NO_PERMISSION = {"error": "This user does not posses the privilege to access this route"}
ACCESS_EXPIRES = timedelta(days=30)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

REDIS_SENTINELS = [('redis-sentinel', 26379),
                   ('redis-sentinel2', 26379),
                   ('redis-sentinel3', 26379),
                   ]
MASTER_NAME = 'redismaster'

sentinel =Sentinel(REDIS_SENTINELS, socket_timeout = 0.1)
master = sentinel.master_for(MASTER_NAME) 
slave = sentinel.slave_for(MASTER_NAME, socket_timeout=0.1)

db = Database(database=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
appService = AppService(db)


"""
REGISTER USER
"""
@users.route("/auth/register", methods=["POST"])
def register():
    """
    Cualquier usuario puede crear una cuenta con un nombre de usuario y contraseña y un rol para el sistema
    Parameters: 'name', 'password', 'rol' (Pasados mediante el body del request como un json)
    Returns:
        result (error): Retorna "LESS_FIELDS_RES", cuando el body no tiene los campos necesarios(name, password, rol)
        result (1): Retorna codigo 1 si el usuario se creo con exito
        result (5000): Retorna codigo 5000 si el nombre de usuario ya existe
    """
    request_data = request.get_json()
    expected_fields = ['name', 'password', 'rol']
    if all(field in request_data for field in expected_fields):
        request_data = request.get_json(force=True)
        return appService.register(request_data)
    else:
        return LESS_FIELDS_RES


"""
LOGIN USER
"""
@users.route("/auth/login", methods=["POST"])
def login():
    '''
    Si el usuario tiene una cuenta en el sistema puede iniciar sesion
    Parameters:'name', 'password' (Pasados mediante el body del request como un json)
    Returns:
        result (error): Retorna "LESS_FIELDS_RES", cuando el body no tiene los campos necesarios(name, password)
        result (error): Retorna "ERROR_INCORRECT_LOGIN", cuando el name y el password no coinciden con un usuario en la base de datos
        result (json): Retorna el token para el usuario
    '''
    request_data = request.get_json()
    expected_fields = ['name', 'password']
    if not all(field in request_data for field in expected_fields):
        return LESS_FIELDS_RES
    else:
        username = request_data["name"]
        password = request_data["password"]
        response = appService.login({"name": username, "password":password}) 
        if response["code"][0] == None:
            return ERROR_INCORRECT_LOGIN  
        else:    
            access_token = create_access_token(identity={"name" : username,"privilige":response["code"][0]})
            return jsonify(access_token=access_token)


"""
LOGOUT USER
"""
@users.route("/auth/logout")
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    master.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")

    
"""
GET USERS
"""
@users.route("/users")
@jwt_required()
def get_users():
    '''
    Si el usuario tiene los permisos, retorna todos los usuarios.
    Parameters:No recibe parametros
    Returns:
        result (error): Retorna "NO_PERMISSION", cuando el usuario no tiene permisos para obtener los usuarios
        result (json): Retorna una lista de todos los usuario
    '''
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 1):
        return appService.get_users()
    else:
        return NO_PERMISSION

 
"""
GET USER BY ID
"""
@users.route("/users/<int:id>")
@jwt_required()
def get_user_by_id(id: int):
    '''
	Si el usuario tiene los permisos, retorna el usuario especificado por el ID.
    Parameters: Recibe el id de usuario
    Returns:
  		result (error): Retorna "NO_PERMISSION",  el usuario no tiene permisos para obtener dicho usuario
	  	result (json): Retorna el usuario solicitado
    '''
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 1):
        return appService.get_user_by_id(id)
    else:
        return NO_PERMISSION
    

"""
UPDATE USER
"""
@users.route("/users/<int:id>", methods=["PUT"])
@jwt_required()
def update_user(id : int):
    '''
        Si el usuario tiene los permisos, puede actualizar/modificar un usuario en especifico
        Parameters: Recibe el ID del usuario
        Returns:
            result (error): retorna "NO_PERMISSION", cuando el usuario no tiene permisos para modificar el usuario
        result (error): retorna LESS_FIELDS_RES, cuando faltan campos en los datos de la solicitud 
            result (json): Si se modifico correctamente se guarda los datos a la base de datos 
    '''
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    expected_fields = ['name', 'password', 'rol']
    request_data = request.get_json(force=True)
    if not all(field in request_data for field in expected_fields):
        return LESS_FIELDS_RES
    else:
        if ((user["sub"]["privilige"] == 1) or (appService.get_user_name_by_id(id)[0] == user["sub"]['name'])):
            request_data["id"] = id
            return appService.update_user(request_data)
        else:
            return NOT_SAME_USER
    
    
"""
DELETE USER
"""
@users.route("/users/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id : int):
    '''
        Si el usuario tiene los permisos, puede eliminar un usuario en especifico
        Parameters: Recibe el ID del usuario
        Returns:
            result (error): retorna "NO_PERMISSION", cuando el usuario no tiene permisos para eliminar el usuario
        result (error): retorna LESS_FIELDS_RES, cuando faltan campos en los datos de la solicitud 
            result (json): Si se elimina correctamente se retorna el usuario
    '''
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 1):
        return {"response": appService.delete_user(id)}
    else:
        return NO_PERMISSION

