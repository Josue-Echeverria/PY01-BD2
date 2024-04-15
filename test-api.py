import unittest
from unittest.mock import patch
import json  # Agregar la importación del módulo json
from app import app, mongo_db

from utils import MongoEnum




class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.ERROR_NO_LOGIN = "{\"error\":\"You have to log in at: http://localhost:5002/\"}\n"
        self.ERROR_LESS_FIELDS = "{\"error\":\"Not the required fields\"}\n"     
        self.ERROR_NO_AUTH_HEADERS = "{\"msg\":\"Missing Authorization Header\"}\n"
        self.ERROR_NO_PERMISSION = "{\"error\":\"This user does not posses the privilege to access this route\"}\n"
        self.ERROR_INCORRECT_CREDENTIALS = "{\"error\":\"Incorrect user or password\"}\n"
        self.ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMjQ0MjY0NiwianRpIjoiODkwNzZjNWQtNDQ1Ni00MjJiLTg3MzUtZGIwZjc2NjBlZWQ0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJuYW1lIjoiY2NjIiwicHJpdmlsaWdlIjoxfSwibmJmIjoxNzEyNDQyNjQ2LCJjc3JmIjoiMGExMDBkMDYtOGE3YS00ZGVjLTgwYzktZjJmMjA4MzY2ODc0IiwiZXhwIjoxNzE1MDM0NjQ2fQ.J36ELRir9jngcHSBnWb2bsxHphRGUw46Z1VGpSWVlRU"
        self.NO_ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMjQ0MzYzNywianRpIjoiNjIwNWMxMWEtNTliZS00NGE1LWJhNWItNThmOWFjNWJiOWEzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJuYW1lIjoiYWFhIiwicHJpdmlsaWdlIjoyfSwibmJmIjoxNzEyNDQzNjM3LCJjc3JmIjoiMjY5ZTM4OTctOTAzNS00OTg5LTk4OWItNjZhMzUxNWZkNTY0IiwiZXhwIjoxNzE1MDM1NjM3fQ.4zYreMIi1axmSsWJYJpzHY_izZloyZ9_0TNPco0sRvo"

        self.ENCUESTADO_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMzIyMDM3MiwianRpIjoiOGExZjE2NjgtNjljNi00ZWFkLWE4OTgtNzc3OTYwNTg3NGRmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJuYW1lIjoiZW5jdWVzdCIsInByaXZpbGlnZSI6M30sIm5iZiI6MTcxMzIyMDM3MiwiY3NyZiI6ImQzMDc3ZjZhLWQ4M2EtNGYzNC1iNTI3LTI1NmFmMjA3ZGYwMiIsImV4cCI6MTcxNTgxMjM3Mn0.06MShqb3bG_nIsGINKljLQQB-CJ2pCVtNeAP9BGOkFE"

        self.NOT_SAME_USER = "{\"error\":\"The id in the request and the id of this user do not coincide\"}\n"

    #Ambiente de prueba
    @classmethod
    def setUpClass(cls):
        cls.create_sample_survey()
        
        
    @classmethod
    def create_sample_survey(cls):
        # Crea un survey de ejemplo en la base de datos de pruebas
        sample_survey = {
            "id_survey": MongoEnum.TEST_ID.value,
            "questions": [
                {"id_question": 1, "text": "¿Cuál es tu color favorito?"},
                {"id_question": 2, "text": "¿Qué deporte practicas?"}
            ]
        }
        mongo_db.db.surveys.insert_one(sample_survey)
    
    @classmethod
    def delete_sample_survey(self):
        # Elimina el survey de ejemplo de la base de datos de pruebas
        mongo_db.db.surveys.delete_one({"id_survey": MongoEnum.TEST_ID.value},)

   

    @classmethod
    def tearDownClass(cls):
        # Limpiar después de todas las pruebas en la clase de prueba
        cls.delete_sample_survey()

   
   
    
   
    # ----- Register tests

    def testLessFieldsRegisterUser(self):
        with self.app as client:
            
            new_user = {
                "name": "nombre del usuario",
                "rol": 1  
            }
            
            response = client.post('/auth/register', json=new_user)  

            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_LESS_FIELDS, response.get_data(as_text=True))


    def testCorrectRegisterUser(self):        
        with self.app as client:
            # Registro de usuario admin
            new_user = {
                "name": "nombre del usuario",
                "password": "contraseña del usuario",
                "rol": 1  
            }
            response = client.post('/auth/register', json=new_user)
            self.assertEqual(response.status_code, 200)
            
            # Registro de creador de encuesta
            new_survey_creator = {
                "name": "creador de encuesta",
                "password": "contraseña",
                "rol": 2 
            }
            response = client.post('/auth/register', json=new_survey_creator)
            self.assertEqual(response.status_code, 200)


    # ----- Login tests
            
    def testIncorrectLogin(self):
        with self.app as client:
            user = {
                "name": "nombre del usuario",
                "password": "contraseña incorrecta del usuario"
            }
            response = client.post('/auth/login', json=user)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_INCORRECT_CREDENTIALS, response.get_data(as_text=True))

    
    def testLessFieldsLogin(self):
        with self.app as client:
          
            user = {
                "name": "nombre del usuario",
            }
            response = client.post('/auth/login', json=user)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_LESS_FIELDS, response.get_data(as_text=True))


    def testCorrectLogin(self):
        with self.app as client:
            
            user = {
                "name": "ccc",
                "password": "qwerty"
            }
            response = client.post('/auth/login', json=user)
            self.assertEqual(response.status_code, 200)
    
    # ----- Users data tests

    def testUnauthorizedGetUsers(self):
        with self.app as client:
            response = client.get('/users', headers={"Authorization": "Bearer "+self.NO_ADMIN_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION, response.get_data(as_text=True))

    def testCorrectGetUsers(self):
        with self.app as client:
            response = client.get('/users', headers={"Authorization": "Bearer "+self.ADMIN_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(self.ERROR_NO_PERMISSION, response.get_data(as_text=True))

    
    # ----- Update users data tests
    def testLessFieldsUpdateUser(self):
        with self.app as client:
            user = {
                "name": "nombre del usuario"
            }
            response = client.put('/users/1', headers={"Authorization": "Bearer "+self.ADMIN_TOKEN},json = user)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_LESS_FIELDS, response.get_data(as_text=True))


    def testUnauthorizedUpdateUser(self):
        with self.app as client:
            user = {
                "name": "ddd",
                "password": "mnbc",
                "rol": 1
            }
            response = client.put('/users/1', headers={"Authorization": "Bearer "+self.NO_ADMIN_TOKEN},json = user)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.NOT_SAME_USER, response.get_data(as_text=True))

   
    def testCorrectUpdate(self):        
        with self.app as client:
            user = {
                "name": "ddd",
                "password": "mnbc",
                "rol": 1
            }
            response = client.put('/users/1', headers={"Authorization": "Bearer "+self.ADMIN_TOKEN},json = user)
            self.assertEqual(response.status_code, 200)

    # ----- Delete users tests

    def testUnauthorizedDeleteUser(self):
        with self.app as client:
            response = client.delete('/users/1', headers={"Authorization": "Bearer "+self.NO_ADMIN_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION, response.get_data(as_text=True))

    
    def testCorrectDeleteUser(self):
        with self.app as client:
            response = client.delete('/users/2', headers={"Authorization":"Bearer "+self.ADMIN_TOKEN})
            self.assertEqual(response.status_code, 200)



    
    
    
    
    
    #------------------------------------------------------- MONGO
   



# ------------------------------------------- QUESTIONS



    def testGetExistingSurveyQuestions(self):

        with self.app as client:
            response = client.get(f'/surveys/{MongoEnum.TEST_ID.value}/questions')

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
            response = client.post(f'/surveys/{survey_id}/questions', json={"questions": questions_to_add})
            
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 401)
            self.assertIn(self.ERROR_NO_AUTH_HEADERS, response.get_data(as_text=True))
            
            
    def testAddQuestionsInvalidUser(self):
        # Datos de ejemplo
        survey_id = '123'
        questions_to_add = [
            {"id_question": 1, "text": "Pregunta 1"},
            {"id_question": 2, "text": "Pregunta 2"}
        ]
        with self.app as client:
            # Llamada al endpoint token de autorización sin privilegios
            response = client.post(f'/surveys/{survey_id}/questions', json={"questions": questions_to_add}, headers={"Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION, response.get_data(as_text=True))
            
            
    def testAddQuestionsNoNewQuestions(self):
        # Datos de ejemplo
        questions_to_add = []  # No hay nuevas preguntas para agregar
        with self.app as client:
            # Llamada al endpoint con token de autorización
            response = client.post(f'/surveys/{MongoEnum.TEST_ID.value}/questions', json={"questions": questions_to_add}, headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.not_added_questions())

    def testAddQuestionsSurveyNotFound(self):
        # Datos de ejemplo
        survey_id = -1212
        questions_to_add = []  
        with self.app as client:
            # Llamada al endpoint con token de autorización
            response = client.post(f'/surveys/{survey_id}/questions', json={"questions": questions_to_add}, headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.survey_not_found(survey_id))

    def testAddQuestionsExistingQuestion(self):
        # Datos de ejemplo
        survey_id = MongoEnum.TEST_ID.value
        questions_to_add = [{"id_question":1, "content":"mock"}] 
         
        with self.app as client:
            
            # Llamada al endpoint con token de autorización
            response = client.post(f'/surveys/{survey_id}/questions', json={"questions": questions_to_add}, headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.not_added_questions())

    def testAddQuestionsSuccessfully(self):
        # Datos de ejemplo
        survey_id = MongoEnum.TEST_ID.value
        questions_to_add = [{"id_question":3, "content":"new question"}] 
         
        with self.app as client:
            
            # Llamada al endpoint con token de autorización
            response = client.post(f'/surveys/{survey_id}/questions', json={"questions": questions_to_add}, headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.added_questions(len(questions_to_add),survey_id))
            
        
 
    def testUpdateQuestionNoHeader(self):
        with app.test_client() as client:
            response = client.put(f'/surveys/{MongoEnum.TEST_ID.value}/questions/1')
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 401)
            self.assertIn(self.ERROR_NO_AUTH_HEADERS, response.get_data(as_text=True))

    def testUpdateQuestionNoPermission(self):
        with app.test_client() as client:
            response = client.put('/surveys/1/questions/1', headers={"Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION, response.get_data(as_text=True))
            
            
    def testUpdateQuestionNotFoundSurvey(self):
        survey_id = -999
        with app.test_client() as client:
            response = client.put(f'/surveys/{survey_id}/questions/1', headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"}, json={"question": {"id_question": 1, "content": "Updated question"}})
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.survey_not_found(survey_id))



    def testUpdateQuestionNotFoundQuestion(self):
        survey_id = MongoEnum.TEST_ID.value
        question_id = -99
        with app.test_client() as client:
            response = client.put(f'/surveys/{survey_id}/questions/{question_id}', headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"}, json={"question": {"id_question": 999, "content": "Updated question"}})
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.not_found_question(question_id,survey_id))
       
    
    
    def testUpdateQuestionSuccessfully(self):
        survey_id = MongoEnum.TEST_ID.value
        question_id = 1
        
        
        with app.test_client() as client:
            # Preparar la base de datos
            # Llamada al endpoint para actualizar la pregunta
            response = client.put(f'/surveys/{survey_id}/questions/{question_id}', headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"}, json={"question": {"id_question": 1, "text": "Updated question"}})
            
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.updated_question(question_id,survey_id))
        
        
    def testDeleteQuestionNoHeader(self):
        with app.test_client() as client:
            response = client.delete(f'/surveys/{MongoEnum.TEST_ID.value}/questions/1')
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 401)
            self.assertIn(self.ERROR_NO_AUTH_HEADERS, response.get_data(as_text=True))

    def testDeleteQuestionNoPermission(self):
        with app.test_client() as client:
            response = client.delete('/surveys/1/questions/1', headers={"Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION, response.get_data(as_text=True))
            
            
    def testDeleteQuestionNotFoundSurvey(self):
        survey_id = -999
        with app.test_client() as client:
            response = client.delete(f'/surveys/{survey_id}/questions/1', headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.survey_not_found(survey_id))



    def testDeleteQuestionNotFoundQuestion(self):
        survey_id = MongoEnum.TEST_ID.value
        question_id = -99
        with app.test_client() as client:
            response = client.delete(f'/surveys/{survey_id}/questions/{question_id}', headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.not_found_question(question_id,survey_id))
       
    
    
    def testDeleteQuestionSuccessfully(self):
        survey_id = MongoEnum.TEST_ID.value
        question_id = 2
        
        
        with app.test_client() as client:
            # Preparar la base de datos
            # Llamada al endpoint para actualizar la pregunta
            response = client.delete(f'/surveys/{survey_id}/questions/{question_id}', headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.deleted_question(question_id,survey_id))
       
       


if __name__ == '__main__':
    unittest.main()
