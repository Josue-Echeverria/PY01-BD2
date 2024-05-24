import unittest
from unittest.mock import patch
import json  # Agregar la importación del módulo json
from app import app
from db_mongo import MongoDB
from utils import MongoEnum
from endpoints.users.users_tests import TestsUsers

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


    # ENCUESTADO -----------------------------------------------

    # ----- create/post  respondents 
    def testCorrectPostRespondents(self):
        with self.app as client:
            respondents = {
                "nombre": "encuestado prueba",
                "password": "contraseña",
                "edad":22  
            }     
            response = client.post(f'/respondents/register', headers={"Authorization": "Bearer " + self.SURVEY},json= respondents)
            self.assertEqual(response.status_code, 200)
            
            respondents = {
                "nombre": "encuestado prueba 2",
                "password": "contraseña",
                "edad":22  
            }     
            response = client.post(f'/respondents/register', headers={"Authorization": "Bearer " + self.SURVEY},json= respondents)
            self.assertEqual(response.status_code, 200)
            respondents = {
                "nombre": "encuestado prueba 3",
                "password": "contraseña",
                "edad":22  
            }     
            response = client.post(f'/respondents/register', headers={"Authorization": "Bearer " + self.SURVEY},json= respondents)
            self.assertEqual(response.status_code, 200) 
    
    def testLessFieldsRespondents(self):
        with self.app as client:
            data = {
                "nombre": "encuestado prueba",
                "edad": 22
                # Falta el campo 'password'
            }     
            response = client.post('/respondents/register', headers={"Authorization": "Bearer " + self.SURVEY}, json=data)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_LESS_FIELDS, response.get_data(as_text=True))

    def testUnauthorizedRespondents(self):
        with self.app as client:
            respondents = {
                "nombre": "encuestado prueba 4",
                "password": "contraseña",
                "edad":22  
            }  
            response = client.post('/respondents/register', headers={"Authorization": "Bearer "+self.ADMIN_TOKEN}, json=respondents)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION, response.get_data(as_text=True))
       
    # ----- get respondents 
    def testGetRespondents(self):
        with self.app as client:
            response = client.get('/respondents', headers={"Authorization": "Bearer "+self.SURVEY})
            self.assertEqual(response.status_code, 200)
    
    def testUnauthorizedGetRespondents(self):
        with self.app as client: 
            response = client.get('/respondents', headers={"Authorization": "Bearer "+self.ADMIN_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION, response.get_data(as_text=True))
   
    # ----- update respondents
    def testUpdateRespondents(self):
        with self.app as client:
            new_respondents = {
                "nombre": "encuestado actualizado", 
                "password": "123",
                "edad": 22
            }
            response = client.put('/respondents/1', headers={"Authorization": "Bearer " + self.SURVEY}, json=new_respondents)
            self.assertEqual(response.status_code, 200)

    def testLessFieldsUpdateRespondents(self):
        with self.app as client:
            data = {
                "nombre": "encuestado no actualizado",
                "edad": 21
                #falta el campo de password 
            }
            response = client.put('/respondents/1', headers={"Authorization": "Bearer "+self.SURVEY},json = data)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_LESS_FIELDS, response.get_data(as_text=True))

    def testUnauthorizedUpdateRespondents(self):
        with self.app as client:
            data = {
                "nombre": "encuestado no actualizado", 
                "password": "123",
                "edad": 22
            }
            response = client.put('/respondents/1', headers={"Authorization": "Bearer "+self.ADMIN_TOKEN},json = data)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION , response.get_data(as_text=True))


    def testDeleteRespondents(self):
        with self.app as client:
            response = client.delete('/respondents/2', headers={"Authorization":"Bearer "+self.SURVEY})
            self.assertEqual(response.status_code, 200)

    def testUnauthorizedDeleteRespondents(self):
        with self.app as client:
            response = client.delete('/respondents/1', headers={"Authorization": "Bearer "+self.ADMIN_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION, response.get_data(as_text=True)) 
    

# ------------------------------------------- SURVEYS


    def testAddSurveyInvalidUser(self):
        survey_to_add = {"id_survey": 10, "name": "encuesta 10",
                         "description": "encuesta de prueba"}

        with self.app as client:
            response = client.post(f'/surveys', json=survey_to_add,
                                   headers={"Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION,
                          response.get_data(as_text=True))

    def testAddSurveyNoName(self):
        survey_to_add = {"id_survey": 10, "description": "encuesta sin nombre"}
        with self.app as client:
            response = client.post(f'/surveys', json=survey_to_add,
                                   headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})

            self.assertEqual(response.status_code, 400)
            self.assertIn("Se requieren los campos 'name' , 'description' y 'id_survey'",
                          response.get_data(as_text=True))

    def testAddSurveyNoDescription(self):
        survey_to_add = {"id_survey": 10, "name": "encuesta 10"}
        with self.app as client:
            response = client.post(f'/surveys', json=survey_to_add,
                                   headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})

            self.assertEqual(response.status_code, 400)
            self.assertIn("Se requieren los campos 'name' , 'description' y 'id_survey'",
                          response.get_data(as_text=True))

    def testAddSurveyNoId(self):
        survey_to_add = {"name": "encuesta 10",
                         "description": "encuesta sin Id"}
        with self.app as client:
            response = client.post(f'/surveys', json=survey_to_add,
                                   headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})

            self.assertEqual(response.status_code, 400)
            self.assertIn("Se requieren los campos 'name' , 'description' y 'id_survey'",
                          response.get_data(as_text=True))

    def testAddSurveyRepeatedId(self):
        survey_to_add = {"id_survey": MongoEnum.TEST_ID.value,
                         "name": "encuesta 10", "description": "encuesta con Id repetido"}
        with self.app as client:
            response = client.post(f'/surveys', json=survey_to_add,
                                   headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})

            self.assertEqual(response.status_code, 200)
            self.assertIn("Ya existe una encuesta con el id_survey",
                          response.get_data(as_text=True))

    def testAddSurveySuccessfully(self):
        survey_to_add = {"id_survey": 55, "name": "encuesta 55",
                         "description": "encuesta sin nombre"}
        with self.app as client:
            response = client.post(f'/surveys', json=survey_to_add,
                                   headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})

            self.assertEqual(response.status_code, 200)

    def testGetAllSurveyInvalidUser(self):
        with self.app as client:
            response = client.get(
                f'/surveys/all', headers={"Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION,
                          response.get_data(as_text=True))

    def testGetAllSurveySuccessfully(self):
        with self.app as client:
            response = client.get(
                f'/surveys/all', headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            self.assertEqual(response.status_code, 200)

    def testGetPublicSurveys(self):
        with self.app as client:
            response = client.get(
                f'/surveys', headers={"Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            self.assertEqual(response.status_code, 200)

    def testGetDetailSurveyInvalidUser(self):
        with self.app as client:
            response = client.get(
                f'/surveys/55', headers={"Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            self.assertEqual(response.status_code, 403)
            self.assertIn("No tiene permiso para acceder a esta encuesta",
                          response.get_data(as_text=True))

    def testGetDetailSurveySuccessfully(self):
        with self.app as client:
            response = client.get(f'/surveys/{MongoEnum.TEST_ID.value}', headers={
                                  "Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            self.assertEqual(response.status_code, 200)

    def testGetDetailSurveyNotFound(self):
        with self.app as client:
            response = client.get(
                f'/surveys/1566', headers={"Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            self.assertEqual(response.status_code, 404)
            self.assertIn("No se encontro la encuesta con id",
                          response.get_data(as_text=True))

    def testModSurveyInvalidUser(self):
        survey_to_modify = {"name": "encuesta 10mod",
                            "description": "encuesta de prueba modificada"}

        with self.app as client:
            response = client.put(f'/surveys/{MongoEnum.TEST_ID.value}', json=survey_to_modify, headers={
                                  "Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION,
                          response.get_data(as_text=True))

    def testModSurveyNoName(self):
        survey_to_modify = {"description": "encuesta de prueba modificada"}
        with self.app as client:
            response = client.put(f'/surveys/{MongoEnum.TEST_ID.value}', json=survey_to_modify, headers={
                                  "Authorization": f"Bearer {self.ADMIN_TOKEN}"})

            self.assertEqual(response.status_code, 400)
            self.assertIn("Se requieren los campos 'name' y 'description'",
                          response.get_data(as_text=True))

    def testModSurveyNoDescription(self):
        survey_to_modify = {"name": "encuesta 10mod"}
        with self.app as client:
            response = client.put(f'/surveys/{MongoEnum.TEST_ID.value}', json=survey_to_modify, headers={
                                  "Authorization": f"Bearer {self.ADMIN_TOKEN}"})

            self.assertEqual(response.status_code, 400)
            self.assertIn("Se requieren los campos 'name' y 'description'",
                          response.get_data(as_text=True))

    def testModSurveyNotFound(self):
        with self.app as client:
            survey_to_modify = {"name": "encuesta 10mod",
                                "description": "encuesta de prueba modificada"}
            response = client.put(f'/surveys/452', json=survey_to_modify,
                                  headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn("No se encontro el id_survey",
                          response.get_data(as_text=True))

    def testPublishSurveyInvalidUser(self):
        with self.app as client:
            response = client.post(f'/surveys/{MongoEnum.TEST_ID.value}/publish', headers={
                                   "Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION,
                          response.get_data(as_text=True))

    def testPublishSurveyAlredyPublic(self):
        with self.app as client:
            response = client.post(f'/surveys/{MongoEnum.TEST_ID.value}/publish', headers={
                                   "Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                f"La encuesta con id_survey: {MongoEnum.TEST_ID.value} ya estaba publica", response.get_data(as_text=True))

    def testPublishSurveyNotFound(self):
        with self.app as client:
            response = client.post(
                f'/surveys/14535/publish', headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn("No se encontro el id_survey: 14535",
                          response.get_data(as_text=True))

    def testHideSurveyInvalidUser(self):
        with self.app as client:
            response = client.post(f'/surveys/{MongoEnum.TEST_ID.value}/hide', headers={
                                   "Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION,
                          response.get_data(as_text=True))

    def testHideSurveySuccessfully(self):
        with self.app as client:
            response = client.post(f'/surveys/{MongoEnum.TEST_ID.value}/hide', headers={
                                   "Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            client.post(f'/surveys/{MongoEnum.TEST_ID.value}/publish',
                        headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                f"Encuesta oculta con id_survey: {MongoEnum.TEST_ID.value}", response.get_data(as_text=True))

    def testHideSurveyAlredyHide(self):
        with self.app as client:
            client.post(f'/surveys/{MongoEnum.TEST_ID.value}/hide',
                        headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            response = client.post(f'/surveys/{MongoEnum.TEST_ID.value}/hide', headers={
                                   "Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            client.post(f'/surveys/{MongoEnum.TEST_ID.value}/publish',
                        headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                f"La encuesta con id_survey: {MongoEnum.TEST_ID.value} ya estaba oculta", response.get_data(as_text=True))

    def testHideSurveyNotFound(self):
        with self.app as client:
            response = client.post(
                f'/surveys/14535/hide', headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn("No se encontro el id_survey: 14535",
                          response.get_data(as_text=True))

    def testDeleteSurveyInvalidUser(self):
        with self.app as client:
            response = client.delete(f'/surveys/{MongoEnum.TEST_ID.value}', headers={
                                     "Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION,
                          response.get_data(as_text=True))

    def testDeleteSurveyNotFound(self):
        with self.app as client:
            response = client.delete(
                f'/surveys/14535', headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn("No se encontro el id_survey: 14535",
                          response.get_data(as_text=True))

    def testDeleteSurveySuccessfully(self):
        survey_to_add = {"id_survey": 80, "name": "encuesta 80",
                         "description": "encuesta de prueba para eliminar"}
        with self.app as client:
            client.post(f'/surveys', json=survey_to_add,
                        headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            response = client.delete(
                f'/surveys/80', headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(f"Encuesta eliminada del id_survey: 80",
                          response.get_data(as_text=True))


# ------------------------------------------- QUESTIONS

    def testGetExistingSurveyQuestions(self):

        with self.app as client:
            response = client.get(
                f'/surveys/{MongoEnum.TEST_ID.value}/questions')

            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('questions', json_response)

    def testNotGetExistingSurveyQuestions(self):
        # Survey inexistente
        survey_id = -456

        with self.app as client:
            response = client.get(f'/surveys/{survey_id}/questions')

            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('error', json_response)
            message = json_response['error']

            # Comparar la lista de preguntas recibida en la respuesta con la lista esperada
            self.assertEqual(message, MongoEnum.survey_not_found(survey_id))

    def testAddQuestionsNoHeader(self):
        # Datos de ejemplo
        survey_id = 123
        questions_to_add = [
            {"id_question": 1, "text": "Pregunta 1"},
            {"id_question": 2, "text": "Pregunta 2"}
        ]
        with self.app as client:
            # Llamada al endpoint sin token de autorización
            response = client.post(
                f'/surveys/{survey_id}/questions', json={"questions": questions_to_add})

            # Verificación de la respuesta
            self.assertEqual(response.status_code, 401)
            self.assertIn(self.ERROR_NO_AUTH_HEADERS,
                          response.get_data(as_text=True))

    def testAddQuestionsInvalidUser(self):
        # Datos de ejemplo
        survey_id = '123'
        questions_to_add = [
            {"id_question": 1, "text": "Pregunta 1"},
            {"id_question": 2, "text": "Pregunta 2"}
        ]
        with self.app as client:
            # Llamada al endpoint token de autorización sin privilegios
            response = client.post(f'/surveys/{survey_id}/questions', json={
                                   "questions": questions_to_add}, headers={"Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})

            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION,
                          response.get_data(as_text=True))

    def testAddQuestionsNoNewQuestions(self):
        # Datos de ejemplo
        questions_to_add = []  # No hay nuevas preguntas para agregar
        with self.app as client:
            # Llamada al endpoint con token de autorización
            response = client.post(f'/surveys/{MongoEnum.TEST_ID.value}/questions', json={
                                   "questions": questions_to_add}, headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})

            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(
                json_response['result'], MongoEnum.not_added_questions())

    def testAddQuestionsSurveyNotFound(self):
        # Datos de ejemplo
        survey_id = -1212
        questions_to_add = []
        with self.app as client:
            # Llamada al endpoint con token de autorización
            response = client.post(f'/surveys/{survey_id}/questions', json={
                                   "questions": questions_to_add}, headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})

            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(
                json_response['result'], MongoEnum.survey_not_found(survey_id))

    def testAddQuestionsExistingQuestion(self):
        # Datos de ejemplo
        survey_id = MongoEnum.TEST_ID.value
        questions_to_add = [{"id_question": 1, "content": "mock"}]

        with self.app as client:

            # Llamada al endpoint con token de autorización
            response = client.post(f'/surveys/{survey_id}/questions', json={
                                   "questions": questions_to_add}, headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})

            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(
                json_response['result'], MongoEnum.not_added_questions())

    def testAddQuestionsSuccessfully(self):
        # Datos de ejemplo
        survey_id = MongoEnum.TEST_ID.value
        questions_to_add = [{"id_question": 3, "content": "new question"}]

        with self.app as client:

            # Llamada al endpoint con token de autorización
            response = client.post(f'/surveys/{survey_id}/questions', json={
                                   "questions": questions_to_add}, headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})

            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.added_questions(
                len(questions_to_add), survey_id))

    def testUpdateQuestionNoHeader(self):
        with app.test_client() as client:
            response = client.put(
                f'/surveys/{MongoEnum.TEST_ID.value}/questions/1')
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 401)
            self.assertIn(self.ERROR_NO_AUTH_HEADERS,
                          response.get_data(as_text=True))

    def testUpdateQuestionNoPermission(self):
        with app.test_client() as client:
            response = client.put(
                '/surveys/1/questions/1', headers={"Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION,
                          response.get_data(as_text=True))

    def testUpdateQuestionNotFoundSurvey(self):
        survey_id = -999
        with app.test_client() as client:
            response = client.put(f'/surveys/{survey_id}/questions/1', headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"}, json={
                                  "question": {"id_question": 1, "content": "Updated question"}})
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(
                json_response['result'], MongoEnum.survey_not_found(survey_id))

    def testUpdateQuestionNotFoundQuestion(self):
        survey_id = MongoEnum.TEST_ID.value
        question_id = -99
        with app.test_client() as client:
            response = client.put(f'/surveys/{survey_id}/questions/{question_id}', headers={
                                  "Authorization": f"Bearer {self.ADMIN_TOKEN}"}, json={"question": {"id_question": 999, "content": "Updated question"}})
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.not_found_question(
                question_id, survey_id))

    def testUpdateQuestionSuccessfully(self):
        survey_id = MongoEnum.TEST_ID.value
        question_id = 1

        with app.test_client() as client:
            # Preparar la base de datos
            # Llamada al endpoint para actualizar la pregunta
            response = client.put(f'/surveys/{survey_id}/questions/{question_id}', headers={
                                  "Authorization": f"Bearer {self.ADMIN_TOKEN}"}, json={"question": {"id_question": 1, "text": "Updated question"}})

            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.updated_question(
                question_id, survey_id))

    def testDeleteQuestionNoHeader(self):
        with app.test_client() as client:
            response = client.delete(
                f'/surveys/{MongoEnum.TEST_ID.value}/questions/1')
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 401)
            self.assertIn(self.ERROR_NO_AUTH_HEADERS,
                          response.get_data(as_text=True))

    def testDeleteQuestionNoPermission(self):
        with app.test_client() as client:
            response = client.delete(
                '/surveys/1/questions/1', headers={"Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION,
                          response.get_data(as_text=True))

    def testDeleteQuestionNotFoundSurvey(self):
        survey_id = -999
        with app.test_client() as client:
            response = client.delete(f'/surveys/{survey_id}/questions/1', headers={
                                     "Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(
                json_response['result'], MongoEnum.survey_not_found(survey_id))

    def testDeleteQuestionNotFoundQuestion(self):
        survey_id = MongoEnum.TEST_ID.value
        question_id = -99
        with app.test_client() as client:
            response = client.delete(f'/surveys/{survey_id}/questions/{question_id}', headers={
                                     "Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.not_found_question(
                question_id, survey_id))

    def testDeleteQuestionSuccessfully(self):
        survey_id = MongoEnum.TEST_ID.value
        question_id = 2

        with app.test_client() as client:
            # Llamada al endpoint para actualizar la pregunta
            response = client.delete(f'/surveys/{survey_id}/questions/{question_id}', headers={
                                     "Authorization": f"Bearer {self.ADMIN_TOKEN}"})

            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.deleted_question(
                question_id, survey_id))

    def testAddAnswersNoHeader(self):
        # Datos de ejemplo
        survey_id = 123
        answers_to_add = {"id_survey": 1, "respondent": 1, "answers":
                          [
                              {"id_question": 1, "text": "Pregunta 1"},
                              {"id_question": 2, "text": "Pregunta 2"}
                          ]}
        with self.app as client:
            # Llamada al endpoint sin token de autorización
            response = client.post(
                f'/surveys/{survey_id}/responses', json=answers_to_add)

            # Verificación de la respuesta
            self.assertEqual(response.status_code, 401)
            self.assertIn(self.ERROR_NO_AUTH_HEADERS,
                          response.get_data(as_text=True))

    def testAddAnswersInvalidUser(self):
        # Datos de ejemplo
        survey_id = 123
        answers_to_add = {"id_survey": 1, "id_respondent": 1, "answers":
                          [
                              {"id_question": 1, "text": "Pregunta 1"},
                              {"id_question": 2, "text": "Pregunta 2"}
                          ]}

        with self.app as client:
            # Llamada al endpoint token de autorización sin privilegios
            response = client.post(f'/surveys/{survey_id}/responses', json={
                                   "answers": answers_to_add}, headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})

            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION,
                          response.get_data(as_text=True))

    def testAddAnswersNoAnswers(self):
        # Datos de ejemplo
        survey_id = MongoEnum.TEST_ID.value
        answers_to_add = {"id_survey": 1, "id_respondent": 1, "answers":
                          []}

        with self.app as client:
            # Llamada al endpoint token de autorización sin privilegios
            response = client.post(f'/surveys/{survey_id}/responses', json=answers_to_add, headers={
                                   "Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})

            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(
                json_response['result'], MongoEnum.not_added_answers())

    def testAddAnswersSurveyNotFound(self):
        # Datos de ejemplo
        survey_id = -1212
        answers_to_add = {"id_survey": 1, "id_respondent": 1, "answers":
                          []}

        with self.app as client:
            # Llamada al endpoint token de autorización sin privilegios
            response = client.post(f'/surveys/{survey_id}/responses', json=answers_to_add, headers={
                                   "Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            json_response = response.get_json()
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            self.assertIn('result', json_response)
            self.assertEqual(
                json_response['result'], MongoEnum.survey_not_found(survey_id))

    def testAddQuestionsSuccessfully(self):
        # Datos de ejemplo
        survey_id = MongoEnum.TEST_ID.value
        answers_to_add = {"id_survey": 1, "id_respondent": 1, "answers":
                          [
                              {"id_question": 1, "text": "Pregunta 1"},
                              {"id_question": 2, "text": "Pregunta 2"}
                          ]}

        with self.app as client:
            # Llamada al endpoint token de autorización sin privilegios
            response = client.post(f'/surveys/{survey_id}/responses', json=answers_to_add, headers={
                                   "Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            json_response = response.get_json()
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            self.assertIn('result', json_response)
            self.assertEqual(
                json_response['result'], MongoEnum.posted_answers(1, survey_id))

    def testGetAnswersNoHeader(self):
        # Datos de ejemplo
        survey_id = 123
        answers_to_add = {"id_survey": 1, "respondent": 1, "answers":
                          [
                              {"id_question": 1, "text": "Pregunta 1"},
                              {"id_question": 2, "text": "Pregunta 2"}
                          ]}
        with self.app as client:
            # Llamada al endpoint sin token de autorización
            response = client.get(
                f'/surveys/{survey_id}/responses', json=answers_to_add)

            # Verificación de la respuesta
            self.assertEqual(response.status_code, 401)
            self.assertIn(self.ERROR_NO_AUTH_HEADERS,
                          response.get_data(as_text=True))

    def testGetAnswersInvalidUser(self):
        # Datos de ejemplo
        survey_id = 123

        with self.app as client:
            # Llamada al endpoint token de autorización sin privilegios
            response = client.get(f'/surveys/{survey_id}/responses', headers={
                                  "Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})

            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION,
                          response.get_data(as_text=True))

    def testGetAnswersSurveyNotFound(self):
        # Datos de ejemplo
        survey_id = -1212

        with self.app as client:
            # Llamada al endpoint token de autorización sin privilegios
            response = client.get(
                f'/surveys/{survey_id}/responses', headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            json_response = response.get_json()
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            self.assertIn('error', json_response)
            self.assertEqual(
                json_response['error'], MongoEnum.survey_not_found(survey_id))

    def testGetAnswersSuccessfully(self):
        # Datos de ejemplo
        survey_id = MongoEnum.TEST_ID.value

        with self.app as client:
            # Llamada al endpoint token de autorización sin privilegios
            response = client.get(
                f'/surveys/{survey_id}/responses', headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            json_response = response.get_json()
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            self.assertIn('result', json_response)

# GET ANALYSIS ON ANSWERS

    def testGetUnauthorizedAnalysis(self):
        with self.app as client:
            response = client.get('/surveys/1/analysis', headers={"Authorization": "Bearer "+self.NO_ADMIN_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION, response.get_data(as_text=True))
    
    def testGetAnalysisSuccesfully(self):
        with self.app as client: 
            response = client.get('/surveys/1/analysis', headers={"Authorization": "Bearer "+self.ADMIN_TOKEN})
            self.assertEqual(response.status_code, 200)
           



if __name__ == '__main__':
    unittest.main()
