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
        self.NOT_SAME_USER = "{\"error\":\"The id in the request and the id of this user do not coincide\"}\n"

    
    
    
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
            new_user = {
                "name": "nombre del usuario",
                "password": "contraseña del usuario",
                "rol": 1  
            }
            response = client.post('/auth/register', json=new_user)
            
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
   
# Datos de ejemplo de la respuesta esperada

    def testGetExistingSurveyQuestions(self):

        # Llamada al endpoint
        with self.app as client:
            response = client.get(f'/surveys/{MongoEnum.TEST_ID.value}/questions')

            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('questions', json_response)


    def testNotGetExistingSurveyQuestions(self):
        # Survey inexistente
        survey_id = '456'

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
        survey_id = '123'
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
            
            
    #TODO ADD encuestado
    
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

    """def test_add_questions_no_param_questions(self):
        with self.app as client:
            # Llamada al endpoint con token de autorización
            response = client.post(f'/surveys/{MongoEnum.TEST_ID.value}/questions', headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 415)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.not_added_questions())
"""


    def testAddQuestionsSurveyNotFound(self):
        # Datos de ejemplo
        survey_id = -1212
        questions_to_add = []  # No hay nuevas preguntas para agregar
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
        questions_to_add = [{"id_question":99, "content":"mock"}] 
         
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
        questions_to_add = [{"id_question":999, "content":"mock"}] 
         
        with self.app as client:
            
            # Llamada al endpoint con token de autorización
            response = client.post(f'/surveys/{survey_id}/questions', json={"questions": questions_to_add}, headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.added_questions(len(questions_to_add),survey_id))
            
            
            #ELIMINAR Y COMPROBAR
            response = client.delete(f'/surveys/{survey_id}/questions/999', json={"questions": questions_to_add}, headers={"Authorization": f"Bearer {self.ADMIN_TOKEN}"})
            self.assertEqual(response.status_code, 200)
        
    
if __name__ == '__main__':
    unittest.main()