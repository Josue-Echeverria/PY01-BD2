import json
import os
import redis

from redis.sentinel import Sentinel 
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager

from endpoints.users.users import users
from endpoints.respondents.respondents import respondents
from endpoints.surveys.surveys import surveys
from endpoints.questions.questions import questions
from endpoints.answers.answers import answers

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

ACCESS_EXPIRES = timedelta(days=30)

"""
REDIS CONFIG
"""
REDIS_SENTINELS = [('redis-sentinel', 26379),
                   ('redis-sentinel2', 26379),
                   ('redis-sentinel3', 26379),
                   ]
MASTER_NAME = 'redismaster'

# Conexion de redis a traves de sentinels
sentinel =Sentinel(REDIS_SENTINELS, socket_timeout = 0.1)
master = sentinel.master_for(MASTER_NAME) 
slave = sentinel.slave_for(MASTER_NAME, socket_timeout=0.1)

app.config['REDIS_SENTINELS'] = REDIS_SENTINELS
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

# Overwrite de la funcion para revisar que un token este vigente 
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    # Se utiliza el slave para realizar la lectura en la base de datos 
    token_in_redis = slave.get(jti) 
    return token_in_redis is not None


app.register_blueprint(users)
app.register_blueprint(respondents)
app.register_blueprint(surveys)
app.register_blueprint(questions)
app.register_blueprint(answers)

"""
HOME
"""
@app.route("/")
def home():
    return "App Works Great!!!"