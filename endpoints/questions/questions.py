from db_mongo import MongoDB
from bson import ObjectId

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, decode_token

NO_PERMISSION = {"error": "This user does not posses the privilege to access this route"}


questions = Blueprint('questions', __name__)
mongo_db = MongoDB()


"""
GET SURVEY QUESTIONS
"""
@questions.route("/surveys/<survey_id>/questions", methods=["GET"])
def get_survey_questions(survey_id):
    
    '''
    Retorna las preguntas relacionadas al id_survey dado.

            Parameters:
                    page (int): La página a ser mostrada
                    size (int): Cantidad de elementos por página
                    survey_id (int): El id del survey

            Returns:
                    result (json): Un json que contiene las preguntas relacionadas al id_survey
    '''
    
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=5, type=int)

    # Calcular el índice de inicio y el índice de fin para la paginación
    start_index = (page - 1) * size
    end_index = start_index + size
    
    # Obtener las preguntas de la encuesta desde la base de datos MongoDB
    data = mongo_db.get_survey_questions(survey_id, start_index, end_index)

    if "error" in data:
        return data
    else:
        return jsonify({"questions": data["questions"]})


"""
ADD QUESTION
"""
@questions.route("/surveys/<survey_id>/questions", methods=["POST"])
@jwt_required()
def add_questions(survey_id):
    
    '''
    Agrega las preguntas relacionadas al id_survey.

            Parameters:
                    questions (list): Un array conteniendo las preguntas a agregar
                    survey_id (int): El id del survey
                    
            Returns:
                    result (list): Un mensaje explicando el resultado de la operación
    '''
    
    
    headers = request.headers
    if get_user_privilege(headers) not in [1,2]:
        return NO_PERMISSION
    
    data = request.get_json(force=True)
    if "questions" in data and isinstance(data["questions"], list):
        result = mongo_db.add_questions(survey_id, data["questions"])
        return jsonify({"result": result})
    else:
        return jsonify({"error": "El campo 'preguntas' es obligatorio y debe ser una lista"}), 400


"""
UPDATE QUESTION
"""
@questions.route("/surveys/<survey_id>/questions/<question_id>", methods=["PUT"])
@jwt_required()
def update_question(survey_id, question_id):
    '''
    Actualiza la pregunta relacionada a ese id_question en el id_survey dado.

            Parameters:
                    question_id (int): El id de pregunta
                    survey_id (int): El id del survey

            Returns:
                    result (str): Un mensaje explicando el resultado de la operación
    '''
    
    headers = request.headers
    if get_user_privilege(headers) not in [1,2]:
        return NO_PERMISSION
    
    request_data = request.get_json(force=True)
    result_message = mongo_db.update_question(survey_id, question_id, request_data["question"])
    return jsonify({"result" : result_message})


"""
DELETE QUESTION
"""
@questions.route("/surveys/<survey_id>/questions/<question_id>", methods=["DELETE"])
@jwt_required()
def delete_question(survey_id, question_id):
    '''
    Elimina la pregunta relacionada a ese id_question en el id_survey dado.

            Parameters:
                    question_id (int):  El id de pregunta
                    survey_id (int): El id del survey

            Returns:
                    result (str): Un mensaje explicando el resultado de la operación
    '''
    headers = request.headers
    
    if get_user_privilege(headers) not in [1,2]:
        return NO_PERMISSION
    
    result_message = mongo_db.delete_question(survey_id, question_id)
    return jsonify({"result": result_message})

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
