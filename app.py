import json
import os
import redis

from app_service import AppService
from db import Database
from datetime import timedelta

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, decode_token, get_jwt

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


db = Database(database=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)

app = Flask(__name__)
appService = AppService(db)
app.secret_key = os.getenv("APP_SECRET_KEY")

app.config['REDIS_CLIENT'] = redis.StrictRedis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv('REDIS_PORT'),
        db=os.getenv('REDIS_DB'),
        decode_responses=True  # Decode responses to strings
    )

# Config with the JWT 
ACCESS_EXPIRES = timedelta(hours=1)
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
    return appService.register(request_data)


@app.route("/auth/login", methods=["POST"])
def login():
    request_data = request.get_json()
    username = request_data["name"]
    password = request_data["password"]
    response = appService.login({"name": username, "password":password}) 
    if response["code"][0] == None:
        return (f"{username} and {password} do not coincide with any user an password")

        
    elif response["code"][3] == 1:
        access_token = create_access_token(identity={"id" : response["code"][0],"privilige":response["code"][3]})
        return jsonify(access_token=access_token)
    
    elif response["code"][3] == 2:
        access_token = create_access_token(identity={"id" : response["code"][0],"privilige":response["code"][3]})
        return jsonify(access_token=access_token)
    
    elif response["code"][3] == 3:
        access_token = create_access_token(identity={"id" : response["code"][0],"privilige":response["code"][3]})
        return jsonify(access_token=access_token)
    
    return {"response": response}



@app.route("/auth/logout")
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")

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


@app.route("/api/tasks", methods=["PUT"])
def update_task():
    request_data = request.get_json()
    return appService.update_task(request_data)


@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    return appService.delete_task(str(id))
