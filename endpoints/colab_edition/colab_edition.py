from db_mongo import MongoDB
from endpoints.colab_edition.kafka import *
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, decode_token

NO_PERMISSION = {"msg": "This user does not posses the privilege to access this route", "OK": False}
NO_CREATOR = {"msg": "You are not the creator of this survey", "OK": False}
NOT_ALLOWED = {"msg": "This user is not allowed in the edition mode of this survey", "OK": False}
ALREADY_ONLINE = {"msg": "This user is already connected to the edition mode", "OK": False}
ALREADY_ALLOWED = {"msg": "This user is already allowed to the edition mode", "OK": False}
NOT_ONLINE = {"msg": "This user is not connected to the edition mode", "OK": False}
NO_VALID_INPUTS = {"msg": "The body sent is doesnt any of the spaces required", "OK": False}

colab_edition = Blueprint('colab_edition', __name__)
mongo_db = MongoDB()
myKafka = kafka()

"""
START EDITION
"""
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


"""
STOP EDITION
"""
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


"""
CONNECT EDITION
"""
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


"""
DISCONNECT EDITION
"""
@colab_edition.route("/surveys/<int:id_survey>/edit/disconnect", methods=["DELETE"])
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


"""
EDIT QUESTION
"""
@colab_edition.route("/surveys/<int:id_survey>/edit/edit_question", methods=["PUT"])
@jwt_required()
def edit_question(id_survey):
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
        myKafka.edit_question(user, id_survey, data["question_id"], result_message["before"], result_message["after"]) 

    return jsonify(result_message)


"""
EDIT SURVEY INFO
"""
@colab_edition.route("/surveys/<int:id_survey>/edit/edit_survey", methods=["PUT"])
@jwt_required()
def edit_survey(id_survey):
    '''
    Verifica los permisos y actualiza la información de una encuesta especifica.

    Parameters:
        id_survey (str): El id del survey

    Returns:
        result (json): Un mensaje explicando el resultado de la operación. 
    '''
    headers = request.headers
    if get_user_privilege(headers) != 2:
        return NO_PERMISSION
    user = get_user_name(headers)
    online = mongo_db.get_online(id_survey)
    if(user not in online):
        return NOT_ONLINE
    data = request.get_json(force=True)
    result_message = mongo_db.edit_survey(user, id_survey, data)
    if(result_message["OK"]):
        myKafka.edit_survey(user, id_survey, result_message["before"], result_message["after"],result_message["column"]) 

    return jsonify(result_message)


"""
GET CHANGES
"""
@colab_edition.route("/surveys/<int:id_survey>/edit/status", methods=["GET"])
@jwt_required()
def get_status(id_survey):
    headers = request.headers
    if get_user_privilege(headers) != 2:
        return NO_PERMISSION
    user = get_user_name(headers)
    online = mongo_db.get_online(id_survey)
    if(user not in online):
        return NOT_ONLINE
    return jsonify(myKafka.get_notifications(id_survey))


"""
AUTHORIZE CREATOR
"""
@colab_edition.route("/surveys/<int:id_survey>/edit/add_creator/<string:add_creator>", methods=["POST"])
@jwt_required()
def auth_creator(id_survey,add_creator):
    # Si el usuario entrando al endpoint es no es un creador de encuestas
    headers = request.headers
    if get_user_privilege(headers) != 2:
        return NO_PERMISSION
    
    # Si el creador de encuestas no es el creador de la encuesta
    user = get_user_name(headers)
    creator = mongo_db.get_survey_creator(id_survey)
    if(user != creator):
        return NO_CREATOR
    
    # Si el usuario ya estaba autorizado 
    allowed = mongo_db.get_allowed(id_survey)
    if(add_creator in allowed):
        return ALREADY_ALLOWED
    
    result_message = mongo_db.auth_creator(id_survey, add_creator)
    
    return jsonify(result_message)


"""
UNAUTHORIZE CREATOR
"""
@colab_edition.route("/surveys/<int:id_survey>/edit/del_creator/<string:del_creator>", methods=["DELETE"])
@jwt_required()
def unauth_creator(id_survey,del_creator):
    # Si el usuario no es un creador de encuestas 
    headers = request.headers
    if get_user_privilege(headers) != 2:
        return NO_PERMISSION
    
    # Si el creador de encuestas entrando al endpoint no es el creador de la encuesta
    user = get_user_name(headers)
    creator = mongo_db.get_survey_creator(id_survey)
    if(user != creator):
        return NO_CREATOR
    
    # Si el usuario esta en linea 
    online = mongo_db.get_online(id_survey)
    if(del_creator in online):
        # Desconectarlo
        mongo_db.register_user_disconnection(id_survey, del_creator)
        
    # Si el usuario ni si quiera estaba autorizado
    allowed = mongo_db.get_allowed(id_survey)
    if(del_creator not in allowed):
        return NOT_ALLOWED
    
    result_message = mongo_db.unauth_creator(id_survey, del_creator)
    
    return jsonify(result_message)


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