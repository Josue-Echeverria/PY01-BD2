import unittest
from unittest.mock import patch
import json  # Agregar la importación del módulo json
from app import app
from db_mongo import MongoDB
from utils import MongoEnum

mongo_db = MongoDB()

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.ERROR_NO_LOGIN = "{\"error\":\"You have to log in at: http://localhost:5002/\"}\n"
        self.ERROR_LESS_FIELDS = "{\"error\":\"Not the required fields\"}\n"
        self.ERROR_NO_AUTH_HEADERS = "{\"msg\":\"Missing Authorization Header\"}\n"
        self.ERROR_NO_PERMISSION = "{\"error\":\"This user does not posses the privilege to access this route\"}\n"
        self.ERROR_INCORRECT_CREDENTIALS = "{\"error\":\"Incorrect user or password\"}\n"
        self.ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNjU4ODYxNCwianRpIjoiNjU1OGY0YjMtNGJhZi00YzdjLWI4YjctNGEwZTk0YzRjN2MxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJuYW1lIjoiYWRtaW4iLCJwcml2aWxpZ2UiOjF9LCJuYmYiOjE3MTY1ODg2MTQsImNzcmYiOiIzMzg0ZDhlYS1mYWFlLTQ1OGYtYjRlZC01Nzg2NjBlMjM3Y2UiLCJleHAiOjE3MTkxODA2MTR9.DtVSU6nSBNE344zQYXc76Qv10aJX-sXyoQz7pVMPP6A"
        self.NO_ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNTM2MTM0MCwianRpIjoiNWY5MzEwMGMtNzcwYi00MWQ2LTk3MDEtOWIzOGFiODBhNTQ0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJuYW1lIjoiZW5jdWVzdGFkbzAiLCJwcml2aWxpZ2UiOjN9LCJuYmYiOjE3MTUzNjEzNDAsImNzcmYiOiJjODFmZDc5Ny0yYTdkLTQyZTctODUyMi1kNWU1YTEyMTVjNDAiLCJleHAiOjE3MTc5NTMzNDB9.gbiRp3S9vUM9YUMWDPqvf5osFy13Pub25fvhCHUlIxA"

        self.ENCUESTADO_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNTg0MDQwMCwianRpIjoiY2E2YmFkM2EtNjAwZi00NThlLTljOTktNDE0MjgwYWE2ODcwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJuYW1lIjoiZW5jdWVzdGFkbzAiLCJwcml2aWxpZ2UiOjN9LCJuYmYiOjE3MTU4NDA0MDAsImNzcmYiOiI2NDczZDhkOS03YTM3LTQ1MjEtYjk4Ni0xZTVkNjhjYzA4YmMiLCJleHAiOjE3MTg0MzI0MDB9.EgaJmZ-sWCSe44E4RzZ8mSi-ZwYyrKnugX9DD5noCXk"

        self.NOT_SAME_USER = "{\"error\":\"The id in the request and the id of this user do not coincide\"}\n"

       # ENCUESTADO
        self.SURVEY ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNjEzMTg4NiwianRpIjoiZWYwNzU5YWYtZGY2My00MmZlLWE4YWYtOTNjNGNmODI4ZTEyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJuYW1lIjoiY3JlYWRvciIsInByaXZpbGlnZSI6Mn0sIm5iZiI6MTcxNjEzMTg4NiwiY3NyZiI6IjMyMDcyZWI4LTljM2ItNDY2ZC04NDJiLTdkNmE4NmQyZTQzNSIsImV4cCI6MTcxODcyMzg4Nn0.bwkvASKosvbE2X0WEXBQ6zgFz_bigZBvefUoU_Qk3z4"

    # Ambiente de prueba
    @classmethod
    def setUpClass(cls):
        cls.create_sample_survey()

    @classmethod
    def create_sample_survey(cls):
        # Crea un survey de ejemplo en la base de datos de pruebas
        sample_survey = {
            "id_survey": MongoEnum.TEST_ID.value,
            "description": "encuesta de ejemplo",
            "name": "encuesta 1",
            "published": True,
            "questions": [
                {"id_question": 1, "text": "¿Cuál es tu color favorito?"},
                {"id_question": 2, "text": "¿Qué deporte practicas?"}
            ]
        }
        mongo_db.db.surveys.insert_one(sample_survey)

        mongo_db.db.answers.insert_one({"id_survey": MongoEnum.TEST_ID.value, "id_respondent": 1, "answers": [
                                       {"id_question": 1, "type": "open", "text": "¿Cómo te llamas?"},]})

    @classmethod
    def delete_sample_survey(self):
        # Elimina el survey de ejemplo de la base de datos de pruebas
        mongo_db.db.surveys.delete_one({"id_survey": MongoEnum.TEST_ID.value},)
        mongo_db.db.surveys.delete_one({"id_survey": 55},)
        mongo_db.db.surveys.delete_one({"id_survey": 80},)

    @classmethod
    def tearDownClass(cls):
        # Limpiar después de todas las pruebas en la clase de prueba
        cls.delete_sample_survey()

