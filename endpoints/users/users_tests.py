import unittest
from unittest.mock import patch
import json  # Agregar la importación del módulo json
from db_mongo import MongoDB
from utils import MongoEnum
from app_test import TestAPI
mongo_db = MongoDB()

class TestUsers(TestAPI):
    
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
