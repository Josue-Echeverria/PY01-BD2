import os
from db_mongo import MongoDB
from endpoints.surveys.consumer import consumer
from endpoints.surveys.producer import connect_user

from bson import ObjectId
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, decode_token

NO_PERMISSION = {"error": "This user does not posses the privilege to access this route"}
NO_CREATOR = {"error": "You are not the creator of this survey"}
KAFKA1 = os.getenv('KAFKA_BROKER1')


colab_edition = Blueprint('colab_edition', __name__)
mongo_db = MongoDB()


@colab_edition.route("/surveys/<int:survey_id>/edit/start", methods=["POST"])
@jwt_required()
def start_colab_edition(survey_id):
    headers = request.headers
    if get_user_privilege(headers) != 2:
        return NO_PERMISSION
    user = get_user_name(headers)
    if(mongo_db.get_survey_creator(survey_id) != user):
        return NO_CREATOR
    
    connect_user(user,KAFKA1, survey_id) 
    # consumer(KAFKA1,survey_id)

    result_message = mongo_db.start_edition(survey_id, user)
    return jsonify({"result" : result_message})


@colab_edition.route("/surveys/<int:survey_id>/edit/stop", methods=["POST"])
@jwt_required()
def stop_colab_edition(survey_id):
    headers = request.headers
    if get_user_privilege(headers) != 2:
        return NO_PERMISSION
    if(mongo_db.get_survey_creator(survey_id) != get_user_name(headers)):
        return NO_CREATOR

    result_message = mongo_db.stop_edition(survey_id)
    return jsonify({"result" : result_message})



@colab_edition.route("/surveys/<int:id>/edit/submit", methods=["POST"])
@jwt_required()
def post_changes():
    print("")


@colab_edition.route("/surveys/<int:id>/edit/status", methods=["GET"])
@jwt_required()
def get_status():
    print("")


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