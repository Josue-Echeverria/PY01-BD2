import json
import os
import redis

from app_service import AppService
from db import Database
from redis.sentinel import Sentinel 
from db_mongo import MongoDB
from bson import ObjectId
from datetime import timedelta
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, decode_token, get_jwt

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Se define el array de sentinels
REDIS_SENTINELS = [('redis-sentinel', 26379),
                   ('redis-sentinel2', 26379),
                   ('redis-sentinel3', 26379),
                   ]
MASTER_NAME = 'redismaster'
# Conexion de redis a traves de sentinels
sentinel =Sentinel(REDIS_SENTINELS, socket_timeout = 0.1)
master = sentinel.master_for(MASTER_NAME) 
slave = sentinel.slave_for(MASTER_NAME, socket_timeout=0.1)


db = Database(database=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)

app = Flask(__name__)
appService = AppService(db)
app.secret_key = os.getenv("APP_SECRET_KEY")
mongo_db = MongoDB()

app.config['REDIS_SENTINELS'] = REDIS_SENTINELS
ACCESS_EXPIRES = timedelta(days=30)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

# Callback function to check if a JWT exists in the redis blocklis 
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = master.get(jti)    
    return token_in_redis is not None


NO_LOGGED_RES = {"error": "You have to log in at: http://localhost:5002/"}
LESS_FIELDS_RES = {"error": "Not the required fields"}
NO_PERMISSION = {"error": "This user does not posses the privilege to access this route"}
NOT_SAME_USER = {"error": "The id in the request and the id of this user do not coincide"}
ERROR_INCORRECT_LOGIN = {"error": "Incorrect user or password"}  


"""
HOME
"""
@app.route("/")
def home():
    return "App Works Great!!!"


"""
REGISTER USER
"""
@app.route("/auth/register", methods=["POST"])
def register():
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
@app.route("/auth/login", methods=["POST"])
def login():
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
@app.route("/auth/logout")
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")

    
"""
GET USERS
"""
@app.route("/users")
@jwt_required()
def get_users():
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
@app.route("/users/<int:id>")
@jwt_required()
def get_user_by_id(id: int):
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
@app.route("/users/<int:id>", methods=["PUT"])
@jwt_required()
def update_user(id : int):
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
@app.route("/users/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id : int):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 1):
        return {"response": appService.delete_user(id)}
    else:
        return NO_PERMISSION


"""
GET RESPONDENTS 
"""
'''
  Si el usuario tiene los permisos, retorna todos los encuestados.
  Parameters:No recibe parametros
  Returns:
    result (error): Retorna "NO_PERMISSION", cuando el usuario no tiene permisos para obtener los encuentados
		result(json): Retorna una lista de todos los encuentados
'''
@app.route("/respondents")
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
@app.route("/respondents/<int:id>")
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
@app.route("/respondents/register", methods=["POST"])
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
@app.route("/respondents/<int:id>", methods=["PUT"])
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
@app.route("/respondents/<int:id>", methods=["DELETE"])
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

"""
GET ANALYSIS
"""
@app.route("/surveys/<int:id>/analysis")
@jwt_required()
def get_analysis(id : int):
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
@app.route("/surveys/all", methods=["GET"])
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
@app.route("/surveys/<survey_id>", methods=["GET"])
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
@app.route("/surveys", methods=["GET"])
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
@app.route("/surveys/<survey_id>/publish", methods=["POST"])
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
@app.route("/surveys/<survey_id>/hide", methods=["POST"])
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
@app.route("/surveys", methods=["POST"])
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
@app.route("/surveys/<survey_id>", methods=["PUT"])
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
@app.route("/surveys/<survey_id>", methods=["DELETE"])
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


"""
GET SURVEY QUESTIONS
"""
@app.route("/surveys/<survey_id>/questions", methods=["GET"])
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
@app.route("/surveys/<survey_id>/questions", methods=["POST"])
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
@app.route("/surveys/<survey_id>/questions/<question_id>", methods=["PUT"])
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
@app.route("/surveys/<survey_id>/questions/<question_id>", methods=["DELETE"])
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



"""
POST ANSWERS
"""
@app.route("/surveys/<survey_id>/responses", methods=["POST"])
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
@app.route("/surveys/<survey_id>/responses", methods=["GET"])
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
