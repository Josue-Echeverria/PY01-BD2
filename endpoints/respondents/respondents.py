
import os

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, decode_token
from redis.sentinel import Sentinel 
from app_service import AppService
from db import Database
from datetime import timedelta


respondents = Blueprint('respondents', __name__)


LESS_FIELDS_RES = {"error": "Not the required fields"}
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
GET RESPONDENTS 
"""
'''
  Si el usuario tiene los permisos, retorna todos los encuestados.
  Parameters:No recibe parametros
  Returns:
    result (error): Retorna "NO_PERMISSION", cuando el usuario no tiene permisos para obtener los encuestados
		result(json): Retorna una lista de todos los encuestados
'''
@respondents.route("/respondents")
@jwt_required()
def get_respondents():
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 2): 
        return appService.get_respondents()
    else:
        return NO_PERMISSION


"""
GET RESPONDENTS BY ID
"""
'''
	Si el usuario tiene los permisos, retorna el encuestado especificado por el ID.
    Parameters: Recibe el id de encuestado
    Returns:
  		result (error): Retorna "NO_PERMISSION",  el usuario no tiene permisos para obtener dicho encuentado
	  	result (json): Retorna el encuestado solicitado
'''
@respondents.route("/respondents/<int:id>")
@jwt_required()
def get_respondents_by_id(id: int):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 2):
        return appService.get_respondents_by_id(id)
    else:
        return NO_PERMISSION
    

"""
POST RESPONDENTS (REGISTER)
"""   
'''
  Si el usuario tiene los permisos, puede registrar un encuestado
    Parameters: No recibe parametros	
    Returns:
		  result (error): retorna "NO_PERMISSION", cuando el usuario no tiene permisos para el registro
      result (error): retorna LESS_FIELDS_RES, cuando faltan campos en los datos de la solicitud
	  	result (json): Si se registro correctamente se guarda los datos a la base de datos
'''
@respondents.route("/respondents/register", methods=["POST"])
@jwt_required()
def register_respondents():
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 2):    
        request_data = request.get_json(force=True) 
        expected_fields = ['nombre', 'password', 'edad']
        if all(field in request_data for field in expected_fields):
            return appService.register_respondents(request_data)
        else:
            return LESS_FIELDS_RES
    else:
        return NO_PERMISSION


"""
UPDATE RESPONDENTS
"""
'''
	Si el usuario tiene los permisos, puede actualizar/modificar un encuestado en especifico
    Parameters: Recibe el ID especifico
    Returns:
		  result (error): retorna "NO_PERMISSION", cuando el usuario no tiene permisos para modificar el encuestado
      result (error): retorna LESS_FIELDS_RES, cuando faltan campos en los datos de la solicitud 
		  result (json): Si se modifico correctamente se guarda los datos a la base de datos 
'''
@respondents.route("/respondents/<int:id>", methods=["PUT"])
@jwt_required()
def update_respondents(id : int):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 2):
        request_data = request.get_json(force=True)
        expected_fields = ['nombre', 'password', 'edad']
        if all(field in request_data for field in expected_fields):
            request_data["id"] = id
            return appService.update_respondents(request_data)
        else:
            return LESS_FIELDS_RES
    else:
        return NO_PERMISSION

"""
DELETE RESPONDENTS
"""
'''
	Si el usuario tiene los permisos, puede eliminar un encuestado en especifico
    Parameters: Recibe el ID especifico
    Returns:
      result (error): retorna "NO_PERMISSION", cuando el usuario no tiene permisos para eliminar el encuestado
	    result (json): Si se elimino correctamente muestra el encuestado eliminado
'''
@respondents.route("/respondents/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_respondents(id : int):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 2):
        return {"response": appService.delete_respondents(id)}
    else:
        return NO_PERMISSION

