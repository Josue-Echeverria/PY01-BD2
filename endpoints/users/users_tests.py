import unittest
from unittest.mock import patch
from app import app



class TestsUsers(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.ERROR_NO_LOGIN = "{\"error\":\"You have to log in at: http://localhost:5002/\"}\n"
        self.ERROR_LESS_FIELDS = "{\"error\":\"Not the required fields\"}\n"
        self.ERROR_NO_PERMISSION = "{\"error\":\"This user does not posses the privilege to access this route\"}\n"
        self.ERROR_INCORRECT_CREDENTIALS = "{\"error\":\"Incorrect user or password\"}\n"
        self.ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNTM1NjQ4NSwianRpIjoiNWUwZmE0ZjYtNDExYS00ZjcxLWI2OTEtZmJmNGY5YWJmNjQ2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJuYW1lIjoiYWRtaW4iLCJwcml2aWxpZ2UiOjF9LCJuYmYiOjE3MTUzNTY0ODUsImNzcmYiOiIzNmQ1ZDZhMS0xNGQ3LTRlOWUtYTUxZi1mOWJkYzExZjg2NTkiLCJleHAiOjE3MTc5NDg0ODV9.4G0ulSd0ztc_-MlWwh8kac2OksrXwfbq9S1gKAGbyzw"
        self.NO_ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNTM2MTM0MCwianRpIjoiNWY5MzEwMGMtNzcwYi00MWQ2LTk3MDEtOWIzOGFiODBhNTQ0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJuYW1lIjoiZW5jdWVzdGFkbzAiLCJwcml2aWxpZ2UiOjN9LCJuYmYiOjE3MTUzNjEzNDAsImNzcmYiOiJjODFmZDc5Ny0yYTdkLTQyZTctODUyMi1kNWU1YTEyMTVjNDAiLCJleHAiOjE3MTc5NTMzNDB9.gbiRp3S9vUM9YUMWDPqvf5osFy13Pub25fvhCHUlIxA"
        self.NOT_SAME_USER = "{\"error\":\"The id in the request and the id of this user do not coincide\"}\n"

    #######################
    # REGISTER USER TESTS #
    #######################
    """
    LESS FIELDS 
    """
    def testLessFieldsRegisterUser(self):
        with self.app as client:

            new_user = {
                "name": "nombre del usuario",
                "rol": 1
            }

            response = client.post('/auth/register', json=new_user)

            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_LESS_FIELDS,
                          response.get_data(as_text=True))
    """
    CORRECT
    """
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


    ###############
    # LOGIN TESTS #
    ###############
    """
    INCORRECT PASSWORD OR USERNAME
    """
    def testIncorrectLogin(self):
        with self.app as client:
            user = {
                "name": "nombre del usuario",
                "password": "contraseña incorrecta del usuario"
            }
            response = client.post('/auth/login', json=user)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_INCORRECT_CREDENTIALS,
                          response.get_data(as_text=True))
    """
    LESS FIELDS 
    """
    def testLessFieldsLogin(self):
        with self.app as client:

            user = {
                "name": "nombre del usuario",
            }
            response = client.post('/auth/login', json=user)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_LESS_FIELDS,
                          response.get_data(as_text=True))
    """
    CORRECT
    """
    def testCorrectLogin(self):
        with self.app as client:
            user = {
                "name": "ccc",
                "password": "qwerty"
            }
            response = client.post('/auth/login', json=user)
            self.assertEqual(response.status_code, 200)


    ###################
    # GET USERS TESTS #
    ###################
    """
    UNAUTHORIZED
    """
    def testUnauthorizedGetUsers(self):
        with self.app as client:
            response = client.get(
                '/users', headers={"Authorization": "Bearer "+self.NO_ADMIN_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION,
                          response.get_data(as_text=True))
    """
    CORRECT
    """
    def testCorrectGetUsers(self):
        with self.app as client:
            response = client.get(
                '/users', headers={"Authorization": "Bearer "+self.ADMIN_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(self.ERROR_NO_PERMISSION,
                             response.get_data(as_text=True))

    ######################
    # UPDATE USERS TESTS #
    ######################
    """
    UNAUTHORIZED
    """
    def testUnauthorizedUpdateUser(self):
        with self.app as client:
            user = {
                "name": "ddd",
                "password": "mnbc",
                "rol": 1
            }
            response = client.put('/users/1', headers={"Authorization": "Bearer "+self.NO_ADMIN_TOKEN}, json=user)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.NOT_SAME_USER, response.get_data(as_text=True))
    """
    LESS FIELDS 
    """
    def testLessFieldsUpdateUser(self):
        with self.app as client:
            user = {
                "name": "nombre del usuario"
            }
            response = client.put('/users/1', headers={"Authorization": "Bearer "+self.ADMIN_TOKEN}, json=user)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_LESS_FIELDS, response.get_data(as_text=True))
    """
    CORRECT
    """
    def testCorrectUpdate(self):
        with self.app as client:
            user = {
                "name": "ddd",
                "password": "mnbc",
                "rol": 1
            }
            response = client.put('/users/1', headers={"Authorization": "Bearer "+self.ADMIN_TOKEN}, json=user)  
            self.assertEqual(response.status_code, 200)

    ######################
    # DELETE USERS TESTS #
    ######################
    """
    UNAUTHORIZED
    """
    def testUnauthorizedDeleteUser(self):
        with self.app as client:
            response = client.delete('/users/1', headers={"Authorization": "Bearer "+self.NO_ADMIN_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION,response.get_data(as_text=True))
                          
    """
    CORRECT
    """
    def testCorrectDeleteUser(self):
        with self.app as client:
            response = client.delete('/users/2', headers={"Authorization": "Bearer "+self.ADMIN_TOKEN})
            self.assertEqual(response.status_code, 200)
