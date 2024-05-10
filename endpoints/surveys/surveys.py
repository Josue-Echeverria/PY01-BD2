from db_mongo import MongoDB
from bson import ObjectId

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, decode_token

NO_PERMISSION = {"error": "This user does not posses the privilege to access this route"}


surveys = Blueprint('survey', __name__)
mongo_db = MongoDB()

"""
GET ANALYSIS
"""
@surveys.route("/surveys/<int:id>/analysis")
@jwt_required()
def get_analysis(id : int):
    '''
    Retorna un analisis detallado de los promedios y los contadores por opcion en las respuestas.

            Parameters:
                    survey_id (int): El id del survey

            Returns:
                    result (json): Un json que contiene la información del analisis
    '''  
    privilege = get_user_privilege(request.headers)
    if ((privilege == 1)):
        return {"response": mongo_db.get_survey_analysis(id)}
    elif ((privilege == 2) and (mongo_db.get_survey_creator(id) == get_user_name(request.headers))):
        return {"response": mongo_db.get_survey_analysis(id)}
    else:
        return NO_PERMISSION


"""
GET SURVEYS
"""
@surveys.route("/surveys/all", methods=["GET"])
@jwt_required()
def get_surveys():
    '''
    Verifica los permisos necesarios para administrador y retorna todas las encuestas disponibles en la base de datos.
            Parameters:
                    page (int): La página a ser mostrada
                    per_page (int): Cantidad de elementos por página
                    
            Returns:
                    result (json): Una colección con las encuestas encontradas.
    '''
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 1 or user["sub"]["privilige"] == 2):
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=5, type=int)
        
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        
        data = mongo_db.get_surveys(start=start_index, end=end_index)
        serialized_data = object_id_to_string(data)
        response = jsonify(serialized_data)

        return response
    else:
        return NO_PERMISSION


"""
GET SURVEYS BY ID
"""
@surveys.route("/surveys/<survey_id>", methods=["GET"])
@jwt_required()   
def get_survey_detail(survey_id):
    '''
    Retorna la información que contiene la encuesta especificada.

            Parameters:
                    survey_id (int): El id del survey

            Returns:
                    result (json): Un json que contiene la información relacionada al id_survey
    '''  
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    survey = mongo_db.get_survey_detail(survey_id)

    if not survey:
        return jsonify({"error": f"No se encontro la encuesta con id {survey_id}"}), 404

    if survey.get("published", False):
        # Si la encuesta está published, cualquier usuario puede acceder a ella
        return jsonify(serialize_object_to_string(survey))
    else:
        # Si la encuesta no está published, solo los usuarios con privilegios 1 o 2 pueden acceder
        if (user["sub"]["privilige"] == 1 or user["sub"]["privilige"] == 2):
            return jsonify(serialize_object_to_string(survey))
        else:
            return jsonify({"error": "No tiene permiso para acceder a esta encuesta"}), 403
        

"""
GET PUBLIC SURVEYS
"""
@surveys.route("/surveys", methods=["GET"])
@jwt_required()   
def get_public_surveys():
        '''
        Retorna las encuestas publicadas en la base de datos.

                Parameters:
                        page (int): Numero de página
                        per_page (int): cantidad de elementos por página

                Returns:
                        surveys (json): Un json que contiene las encuestas públicas
        '''        
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=5, type=int)
        
        start_index = (page - 1) * per_page
        end_index = start_index + per_page        
        data = mongo_db.get_public_surveys(start=start_index, end=end_index)
        serialized_data = object_id_to_string(data)
        return jsonify(serialized_data)


"""
POST PUBLISHED SURVEY 
"""
@surveys.route("/surveys/<survey_id>/publish", methods=["POST"])
@jwt_required() 
def show_survey(survey_id):
    '''
    Verifica los permisos y publica una encuesta modificando su valor "published" a True una encuesta especifica.

            Parameters:
                    survey_id (int): El id del survey

            Returns:
                    result (json): Un mensaje explicando el resultado de la operación.
                    error (str): Un mensaje de error si no se publicó la encuesta
    '''
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 1 or user["sub"]["privilige"] == 2):
        survey_id = mongo_db.show_survey(survey_id)
        return jsonify({"Publicando ": str(survey_id)})
    else:
        return NO_PERMISSION
    

"""
POST HIDE SURVEY
"""
@surveys.route("/surveys/<survey_id>/hide", methods=["POST"])
@jwt_required() 
def hide_survey(survey_id):
    '''
    Verifica los permisos y oculta una encuesta modificando su valor "published" a False una encuesta especifica.

            Parameters:
                    survey_id (int): El id del survey

            Returns:
                    result (json): Un mensaje explicando el resultado de la operación.
                    error (str): Un mensaje de error si no se publicó la encuesta
    '''
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 1 or user["sub"]["privilige"] == 2):
        survey_id = mongo_db.hide_survey(survey_id)
        return jsonify({"Ocultando ": str(survey_id)})
    else:
        return NO_PERMISSION


"""
ADD SURVEY
"""
@surveys.route("/surveys", methods=["POST"])
@jwt_required()
def add_survey():
    '''
    Crea una nueva encuesta con los datos proporcionados y crea el campo "published" por defecto en False.

            Parameters:
                    data (json): Información de la encuesta a agregar con "name", "description" y "id_survey"


            Returns:
                    questions (json): Un json que contiene la confirmación en el id de creación
                    error (str): Un mensaje de error si ya esxiste el id_survey
    '''
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 1 or user["sub"]["privilige"] == 2):
        data = request.json
        if "name" not in data or "description" not in data or "id_survey" not in data:
            return jsonify({"error": "Se requieren los campos 'name' , 'description' y 'id_survey'"}), 400
        
        data.setdefault("published", False)
        survey_id = mongo_db.add_survey(data)
        return jsonify({"Agregando ": str(survey_id)})
    else:
        return NO_PERMISSION
    

"""
UPDATE SURVEY
"""
@surveys.route("/surveys/<survey_id>", methods=["PUT"])
@jwt_required()
def update_survey(survey_id):
    '''
    Verifica los permisos y actualiza la información de una encuesta especifica.

            Parameters:
                    data (json): información nueva de la encuesta
                    survey_id (int): El id del survey

            Returns:
                    result (json): Un mensaje explicando el resultado de la operación.
                    error (str): Un mensaje de error si no se actualizó la encuesta

    '''
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 1 or user["sub"]["privilige"] == 2):
        data = request.json
        if "name" not in data or "description" not in data:
            return jsonify({"error": "Se requieren los campos 'name' y 'description'"}), 400
        
        data.setdefault("published", False)
        survey_id = mongo_db.update_survey(survey_id,data)
        return jsonify({"Actualizando ": str(survey_id)})
    else:
        return NO_PERMISSION
    

"""
DELETE SURVEY
"""
@surveys.route("/surveys/<survey_id>", methods=["DELETE"])
@jwt_required()   
def delete_survey(survey_id):
    '''
    Verifica los permisos del usuario y elimina una encuesta especifica.

            Parameters:
                    survey_id (int): El id del survey

            Returns:
                    result (json): Un mensaje explicando el resultado de la operación.
                    error (str): Un mensaje de error si no se eliminó la encuesta
    '''
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)

    if (user["sub"]["privilige"] == 1 or user["sub"]["privilige"] == 2):
        survey_id = mongo_db.delete_survey(survey_id)
        return jsonify({"Eliminando": str(survey_id)})
    else:
        return NO_PERMISSION


def serialize_object_to_string(data):
    '''
    Retorna los datos sin el campo _id de Mongo

            Parameters:
                    data (list): Una lista con los datos necesarios

            Returns:
                    data (list): La lista filtrada sin el campo _id
    '''
    for key, value in data.items():
        if isinstance(value, ObjectId):
            data[key] = str(value)
    return data


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


def object_id_to_string(data):
    '''
    Retorna los datos sin el campo _id de Mongo

            Parameters:
                    data (list): Una lista con los datos necesarios

            Returns:
                    data (list): La lista filtrada sin el campo _id
    '''
    
    for item in data:
        if '_id' in item:
            item['_id'] = str(item['_id'])
    return data
    