import json
import os
import redis
import subprocess
from redis.sentinel import Sentinel 
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager

from endpoints.users.users import users
from endpoints.respondents.respondents import respondents
from endpoints.surveys.surveys import surveys
from endpoints.colab_edition.colab_edition import colab_edition
from endpoints.questions.questions import questions
from endpoints.answers.answers import answers
from neo4j_app import neo4j_app 

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

ACCESS_EXPIRES = timedelta(days=30)

app.config['REDIS_CLIENT'] = redis.StrictRedis(
        host=os.getenv("REDIS_HOST"),
        port=os.getenv('REDIS_PORT'),
        db=os.getenv('REDIS_DB'),
        decode_responses=True  # Decode responses to strings
    )

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

jwt_redis_blocklist = redis.StrictRedis(
    host=os.getenv("REDIS_HOST")
    , port=os.getenv('REDIS_PORT')
    , db=os.getenv('REDIS_DB')
    , decode_responses=True)


# Overwrite de la funcion para revisar que un token este vigente 
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    # Se utiliza el slave para realizar la lectura en la base de datos 
    token_in_redis = jwt_redis_blocklist.get(jti) 
    return token_in_redis is not None

app.register_blueprint(users)
app.register_blueprint(respondents)
app.register_blueprint(surveys)
app.register_blueprint(questions)
app.register_blueprint(answers)
app.register_blueprint(colab_edition)
app.register_blueprint(neo4j_app) 

"""
HOME
"""
@app.route("/")
def home():
    return "App Works Great!!!"

if __name__ == '__main__':
    subprocess.Popen(['streamlit', 'run', 'streamlit_app.py', '--server.port=8501', '--server.address=0.0.0.0'])
    
    app.run(host='0.0.0.0', port=5000)
