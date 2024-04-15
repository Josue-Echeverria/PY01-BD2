import json
import os
import redis

from app_service import AppService
from db import Database

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
DB_RESPONDENTS = os.getenv("DB_RESPONDENTS")


db = Database(database=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT, respondents=DB_RESPONDENTS)

app = Flask(__name__)
appService = AppService(db)
app.secret_key = os.getenv("APP_SECRET_KEY")
mongo_db = MongoDB()


app.config['REDIS_CLIENT'] = redis.StrictRedis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv('REDIS_PORT'),
        db=os.getenv('REDIS_DB'),
        decode_responses=True  # Decode responses to strings
    )

# Config with the JWT 
ACCESS_EXPIRES = timedelta(days=30)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)
jwt_redis_blocklist = redis.StrictRedis(host=os.getenv("REDIS_HOST"), port=os.getenv('REDIS_PORT'), db=os.getenv('REDIS_DB'), decode_responses=True)

# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


NO_LOGGED_RES = {"error": "You have to log in at: http://localhost:5002/"}
LESS_FIELDS_RES = {"error": "Not the required fields"}
NO_PERMISSION = {"error": "This user does not posses the privilege to access this route"}

@app.route("/")
def home():
    return "App Works Great!!!"


@app.route("/auth/register", methods=["POST"])
def register():
    request_data = request.get_json()
    expected_fields = ['name', 'password', 'rol']
    if all(field in request_data for field in expected_fields):
        request_data = request.get_json(force=True)
        return appService.register(request_data)
    else:
        return LESS_FIELDS_RES


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
            return {"error": "Incorrect user or password"}    
        else:    
            access_token = create_access_token(identity={"name" : username,"privilige":response["code"][0]})
            return jsonify(access_token=access_token)
        
        # This return should never happen 
        # return {"response": response}



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
    if (user["sub"]["privilige"] == 1):
        request_data = request.get_json(force=True)
        expected_fields = ['name', 'password', 'rol']
        if all(field in request_data for field in expected_fields):
            request_data["id"] = id
            return appService.update_user(request_data)
        else:
            return LESS_FIELDS_RES
    else:
        return NO_PERMISSION
    
    
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

#-------------------------------------------------------------------------------------------------------------------
# ENCUESTADO
   
"""
GET RESPONDENTS 
"""
@app.route("/respondents")
@jwt_required()
def get_respondents():
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 2): # x vver si el decode privilege = 2
        return appService.get_respondents()
    else:
        return NO_PERMISSION

"""
GET RESPONDENTS BY ID
"""
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
@app.route("/respondents/register", methods=["POST"])
def register_respondents():
    request_data = request.get_json()
    expected_fields = ['nombre', 'password', 'edad']
    if all(field in request_data for field in expected_fields):
        request_data = request.get_json(force=True)
        return appService.register_respondents(request_data)
    else:
        return LESS_FIELDS_RES

"""
UPDATE RESPONDENTS
"""

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





# -------------------------------------     MONGO


def convert_object_ids(data):
    for item in data:
        if '_id' in item:
            item['_id'] = str(item['_id'])
    return data

# Función para convertir ObjectId a cadena en un diccionario
def serialize_object_ids(data):
    for key, value in data.items():
        if isinstance(value, ObjectId):
            data[key] = str(value)
    return data

@app.route("/surveys/all", methods=["GET"])
@jwt_required()
def get_surveys():

    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 1 or user["sub"]["privilige"] == 2):
            data = mongo_db.get_surveys()
            serialized_data = convert_object_ids(data)
            return jsonify(serialized_data)
    else:
        return NO_PERMISSION


# En tu función get_survey_detail
@app.route("/surveys/<survey_id>", methods=["GET"])
@jwt_required()   
def get_survey_detail(survey_id):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    survey = mongo_db.get_survey_detail(survey_id)

    if not survey:
        return jsonify({"error": f"No se encontró la encuesta con id {survey_id}"}), 404

    if survey.get("published", False):
        # Si la encuesta está published, cualquier usuario puede acceder a ella
        return jsonify(serialize_object_ids(survey))
    else:
        # Si la encuesta no está published, solo los usuarios con privilegios 1 o 2 pueden acceder
        if (user["sub"]["privilige"] == 1 or user["sub"]["privilige"] == 2):
            return jsonify(serialize_object_ids(survey))
        else:
            return jsonify({"error": "No tiene permiso para acceder a esta encuesta"}), 403
        
@app.route("/surveys", methods=["GET"])
@jwt_required()   
def get_public_surveys():
        data = mongo_db.get_public_surveys()
        serialized_data = convert_object_ids(data)
        return jsonify(serialized_data)

@app.route("/surveys/<survey_id>/publish", methods=["POST"])
@jwt_required() 
def show_survey(survey_id):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 1 or user["sub"]["privilige"] == 2):
        survey_id = mongo_db.show_survey(survey_id)
        return jsonify({"Publicando ": str(survey_id)})
    else:
        return NO_PERMISSION
    
@app.route("/surveys/<survey_id>/hide", methods=["POST"])
@jwt_required() 
def hide_survey(survey_id):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)
    if (user["sub"]["privilige"] == 1 or user["sub"]["privilige"] == 2):
        survey_id = mongo_db.hide_survey(survey_id)
        return jsonify({"Ocultando ": str(survey_id)})
    else:
        return NO_PERMISSION

@app.route("/surveys", methods=["POST"])
@jwt_required()
def add_survey():
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
    
@app.route("/surveys/<survey_id>", methods=["PUT"])
@jwt_required()
def update_survey(survey_id):
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
    
@app.route("/surveys/<survey_id>", methods=["DELETE"])
@jwt_required()   
def delete_survey(survey_id):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    user = decode_token(token)

    if (user["sub"]["privilige"] == 1 or user["sub"]["privilige"] == 2):
        survey_id = mongo_db.delete_survey(survey_id)
        return jsonify({"Eliminando": str(survey_id)})
    else:
        return NO_PERMISSION


@app.route("/surveys/<survey_id>/questions", methods=["GET"])
def get_survey_by_id(survey_id):
    data = mongo_db.get_survey_questions(survey_id)
    return jsonify({"result":data})



@app.route("/surveys/<survey_id>/questions", methods=["POST"])
@jwt_required()
def agregar_preguntas(survey_id):
    data = request.json
    
    if "questions" in data and isinstance(data["questions"], list):
        result = mongo_db.add_questions(survey_id, data["questions"])
    
        return jsonify({"result": result})
    else:
        return jsonify({"error": "El campo 'preguntas' es obligatorio y debe ser una lista"}), 400



@app.route("/surveys/<survey_id>/questions/<question_id>", methods=["PUT"])
@jwt_required()
def update_question(survey_id, question_id):
    request_data = request.get_json(force=True)
    
    result_message = mongo_db.update_question(survey_id, question_id, request_data["question"])
    
    return jsonify({"result" : result_message})


@app.route("/surveys/<int:survey_id>/questions/<int:question_id>", methods=["DELETE"])
@jwt_required()
def delete_question(survey_id, question_id):
    
    result_message = mongo_db.delete_question(survey_id, question_id)
    
    return jsonify({"message": result_message})

