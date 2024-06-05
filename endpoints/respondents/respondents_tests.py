import unittest
from unittest.mock import patch
import json  # Agregar la importación del módulo json
from db_mongo import MongoDB
from utils import MongoEnum
from app_test import TestAPI
mongo_db = MongoDB()


class TestRespondents(TestAPI):

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
    
