import unittest
import json  # Agregar la importación del módulo json
from app import app


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.USER_TEST = 'Kevin'
        self.PASS_TEST = 'holamundo'
        self.ERROR_NO_LOGIN = "{\"error\":\"You have to log in at: http://localhost:5002/\"}\n"
        self.ERROR_LESS_FIELDS = "{\"error\":\"Not the required fields\"}\n"
        self.ERROR_NO_PERMISSION = "{\"error\":\"This user does not posses the privilege to access this route\"}\n"
        self.ERROR_INCORRECT_CREDENTIALS = "{\"error\":\"Incorrect user or password\"}\n"
        self.ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMjQ0MjY0NiwianRpIjoiODkwNzZjNWQtNDQ1Ni00MjJiLTg3MzUtZGIwZjc2NjBlZWQ0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJuYW1lIjoiY2NjIiwicHJpdmlsaWdlIjoxfSwibmJmIjoxNzEyNDQyNjQ2LCJjc3JmIjoiMGExMDBkMDYtOGE3YS00ZGVjLTgwYzktZjJmMjA4MzY2ODc0IiwiZXhwIjoxNzE1MDM0NjQ2fQ.J36ELRir9jngcHSBnWb2bsxHphRGUw46Z1VGpSWVlRU"
        self.NO_ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxMjQ0MzYzNywianRpIjoiNjIwNWMxMWEtNTliZS00NGE1LWJhNWItNThmOWFjNWJiOWEzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJuYW1lIjoiYWFhIiwicHJpdmlsaWdlIjoyfSwibmJmIjoxNzEyNDQzNjM3LCJjc3JmIjoiMjY5ZTM4OTctOTAzNS00OTg5LTk4OWItNjZhMzUxNWZkNTY0IiwiZXhwIjoxNzE1MDM1NjM3fQ.4zYreMIi1axmSsWJYJpzHY_izZloyZ9_0TNPco0sRvo"
    
    
    
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

    def testUnauthorizedUpdateUser(self):
        with self.app as client:
            response = client.put('/users/1', headers={"Authorization": "Bearer "+self.NO_ADMIN_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION, response.get_data(as_text=True))

    def testLessFieldsUpdateUser(self):
        with self.app as client:
            user = {
                "name": "nombre del usuario"
            }
            response = client.put('/users/1', headers={"Authorization": "Bearer "+self.ADMIN_TOKEN},json = user)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_LESS_FIELDS, response.get_data(as_text=True))


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


        
      

if __name__ == '__main__':
    unittest.main()