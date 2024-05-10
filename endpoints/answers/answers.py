from db_mongo import MongoDB
from bson import ObjectId

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, decode_token

NO_PERMISSION = {"error": "This user does not posses the privilege to access this route"}


answers = Blueprint('answers', __name__)
mongo_db = MongoDB()

"""
POST ANSWERS
"""
@answers.route("/surveys/<survey_id>/responses", methods=["POST"])
@jwt_required()
def post_answers(survey_id):
    '''
        Agrega las respuestas de un encuestado en base relacionadas a una encuesta.

                Parameters:
                        respondent_id (int): El id del encuestado
                        answers (list): Un array con todas las respuestas del encuestado
                        survey_id (int): El id del survey

                Returns:
                        result (str): Un mensaje explicando el resultado de la operación
    '''
    headers = request.headers
    if get_user_privilege(headers) != 3: #SI NO ES UN ENCUESTADO
        return NO_PERMISSION
    
    data = request.get_json(force=True)
    if "answers" not in data or not isinstance(data["answers"], list):
        return jsonify({"error": "El campo 'answers' es obligatorio y debe ser una lista"}), 400
    if "id_respondent" not in data:
        return jsonify({"error": "El campo 'id_respondent' es obligatorio"}), 400
    
    result = mongo_db.post_answers(survey_id, data["id_respondent"], data["answers"])
    return jsonify({"result": result})
    
    
"""
GET ANSWERS
"""    
@answers.route("/surveys/<survey_id>/responses", methods=["GET"])
@jwt_required()
def get_answers(survey_id):
    '''
    Retorna todas las respuestas de un survey 

            Parameters:
                    page (int): La página a ser mostrada
                    size (int): Cantidad de elementos por página
                    survey_id (int): El id del survey

            Returns:
                    result (json): Un json que contiene las respuestas relacionadas al id_survey
    '''
    
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=5, type=int)
    start_index = (page - 1) * size
    end_index = start_index + size
    headers = request.headers
    
    if get_user_privilege(headers) not in [1,2]:
        return NO_PERMISSION
    
    data = mongo_db.get_answers(survey_id, start_index, end_index)
    
    if("error" in data):
        return data 
    else:
        return jsonify({"result" : data})


"""
MODULOS IMPORTANTES
"""

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

