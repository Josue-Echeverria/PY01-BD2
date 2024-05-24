import os
from db_mongo import MongoDB
from endpoints.surveys.kafka import *
from threading import Thread
from bson import ObjectId
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, decode_token

NO_PERMISSION = {"msg": "This user does not posses the privilege to access this route", "OK": False}
NO_CREATOR = {"msg": "You are not the creator of this survey", "OK": False}
NOT_ALLOWED = {"msg": "This user is not allowed in the edition mode of this survey", "OK": False}
ALREADY_ONLINE = {"msg": "This user is already connected to the edition mode", "OK": False}
NOT_ONLINE = {"msg": "This user is not connected to the edition mode", "OK": False}


colab_edition = Blueprint('colab_edition', __name__)
mongo_db = MongoDB()
myKafka = kafka()


@colab_edition.route("/surveys/<int:id_survey>/edit/start", methods=["POST"])
@jwt_required()
def start_colab_edition(id_survey):
    headers = request.headers
    if get_user_privilege(headers) != 2:
        return NO_PERMISSION
    user = get_user_name(headers)
    if(mongo_db.get_survey_creator(id_survey) != user):
        return NO_CREATOR
    
    # Se registra la conexion 
    result_message = mongo_db.start_edition(id_survey, user)

    if(result_message["OK"]):
        myKafka.connect_user(user, id_survey) 

    return jsonify(result_message)


@colab_edition.route("/surveys/<int:id_survey>/edit/stop", methods=["POST"])
@jwt_required()
def stop_colab_edition(id_survey):
    headers = request.headers
    if get_user_privilege(headers) != 2:
        return NO_PERMISSION
    if(mongo_db.get_survey_creator(id_survey) != get_user_name(headers)):
        return NO_CREATOR

    result_message = mongo_db.stop_edition(id_survey)
    if(result_message["OK"]):
        myKafka.stop_edition(id_survey) 

    return jsonify(result_message)


@colab_edition.route("/surveys/<int:id_survey>/edit/connect", methods=["POST"])
@jwt_required()
def connect_colab_edition(id_survey):
    headers = request.headers
    if get_user_privilege(headers) != 2:
        return NO_PERMISSION
    user = get_user_name(headers)
    allowed = mongo_db.get_allowed(id_survey)
    if(user not in allowed):
        return NOT_ALLOWED
    online = mongo_db.get_online(id_survey)
    if(user in online):
        return ALREADY_ONLINE
    result_message = mongo_db.register_user_connection(id_survey, user)
    if(result_message["OK"]):
        myKafka.connect_user(user, id_survey) 

    return jsonify(result_message)


@colab_edition.route("/surveys/<int:id_survey>/edit/disconnect", methods=["POST"])
@jwt_required()
def disconnect_colab_edition(id_survey):
    headers = request.headers
    if get_user_privilege(headers) != 2:
        return NO_PERMISSION
    user = get_user_name(headers)

    result_message = mongo_db.register_user_disconnection(id_survey, user)
    if(result_message["OK"]):
        myKafka.disconnect_user(user, id_survey) 

    return jsonify(result_message)


@colab_edition.route("/surveys/<int:id_survey>/edit/update_question", methods=["POST"])
@jwt_required()
def post_changes(id_survey):
    headers = request.headers
    if get_user_privilege(headers) != 2:
        return NO_PERMISSION
    user = get_user_name(headers)
    online = mongo_db.get_online(id_survey)
    if(user not in online):
        return NOT_ONLINE
    data = request.get_json(force=True)
    
    result_message = mongo_db.edit_question(user, id_survey, data["question_id"], data["new_question"])
    if(result_message["OK"]):
        myKafka.update_question(user, id_survey, data["question_id"], result_message["before"], result_message["after"]) 

    return jsonify(result_message)


@colab_edition.route("/surveys/<int:id_survey>/edit/status", methods=["GET"])
def get_status(id_survey):
     

    return jsonify(myKafka.get_notifications(id_survey))


def get_user_name(headers):
    '''
    Devuelve el nombre de usuario encontrado en la solicitud.

            Parameters:
                    headers (json): Los encabezados de la solicitud

            Returns
                    result (str): El nombre de usuario asociado a la solicitud

    '''
    
    bearer = headers.get('Authorization')
    if bearer:
        token = bearer.split()[1]
        user = decode_token(token)
        return user.get("sub", {}).get("name")
    return None


def get_user_privilege(headers):
    '''
    Retorna el tipo de privilegio encontrado en el header
    1 Administrador
    2 Creador de encuesta
    3 Encuestado

            Parameters:
                    headers (json): Los encabezados de la solicitud

            Returns:
                    result (int): El número del tipo de privilegio
    '''
    bearer = headers.get('Authorization')
    if bearer:
        token = bearer.split()[1]
        user = decode_token(token)
        return user.get("sub", {}).get("privilige")
    return None