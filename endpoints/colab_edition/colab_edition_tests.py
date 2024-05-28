import unittest
from unittest.mock import patch
from app import app
import json


class TestColabEdition(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        self.NEW_CREATOR_NAME = "creador1"
        self.CREATOR_NAME = "creador"
        self.CREATOR_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNjg0ODY4NiwianRpIjoiODllNDZmNjAtMWI1Ni00ZDAzLWExYTQtYmQ3ODRmZTI2ODg4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJuYW1lIjoiY3JlYWRvciIsInByaXZpbGlnZSI6Mn0sIm5iZiI6MTcxNjg0ODY4NiwiY3NyZiI6Ijc4NTBlODM1LThlNDAtNGUyMy05Yzg3LTM0ZmUzOTg0MDM4NCIsImV4cCI6MTcxOTQ0MDY4Nn0.7dmZ5UIIpj4nimjszvd5w3-7JWopKYFP_dbVTIhJylk"
        self.DIFFERENT_CREATOR_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNjg0ODE3NiwianRpIjoiMTU0OGU2NTktYzBhZi00YTY0LWFmMjAtOWRlZjMxNzhmNjg1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJuYW1lIjoiY3JlYWRvcjEiLCJwcml2aWxpZ2UiOjJ9LCJuYmYiOjE3MTY4NDgxNzYsImNzcmYiOiJiMjM2OGQ4ZC1lYjViLTQzMDktOTk0Ny0yYjVmMTFhOTg0NzAiLCJleHAiOjE3MTk0NDAxNzZ9.MtYM4-p3NEreGH_k9bPlW-2381-wP04eFvkivBLZSmI"
        # (Encuestado o Admin)
        self.UNAUTHORIZED_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNTM2MTM0MCwianRpIjoiNWY5MzEwMGMtNzcwYi00MWQ2LTk3MDEtOWIzOGFiODBhNTQ0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJuYW1lIjoiZW5jdWVzdGFkbzAiLCJwcml2aWxpZ2UiOjN9LCJuYmYiOjE3MTUzNjEzNDAsImNzcmYiOiJjODFmZDc5Ny0yYTdkLTQyZTctODUyMi1kNWU1YTEyMTVjNDAiLCJleHAiOjE3MTc5NTMzNDB9.gbiRp3S9vUM9YUMWDPqvf5osFy13Pub25fvhCHUlIxA"
        self.DISCONNECTED = {"msg":"Usuario desconectado", "OK": True}
        self.CONNECTED = {"msg":"Usuario registrado", "OK": True}
        self.NOT_CONNECTED = {"msg":"El usuario no estaba conectado", "OK": False}
        self.NO_PERMISSION = {"msg": "This user does not posses the privilege to access this route", "OK": False}
        self.NO_CREATOR = {"msg": "You are not the creator of this survey", "OK": False}
        self.NOT_ALLOWED = {"msg": "This user is not allowed in the edition mode of this survey", "OK": False}
        self.ALREADY_ONLINE = {"msg": "This user is already connected to the edition mode", "OK": False}
        self.ALREADY_ALLOWED = {"msg": "This user is already allowed to the edition mode", "OK": False}
        self.NOT_ONLINE = {"msg": "This user is not connected to the edition mode", "OK": False}
        self.UPDATED = {"msg":"Cambios aplicados", "OK": True}

        self.NO_UPDATES = {"OK": True,"msg": ["No changes in the last 30 seconds"]}
        self.UPDATES= {"OK": True,"msg": ["creador se ha desconectado","El modo edicion edicion del survey ha terminado, ningun usuario podra editar el survey","creador se ha conectado"]}

        self.QUESTION_UPDATE = {
            "question_id":1,
            "new_question":{
            "id_question": 1,
            "question_text": "What makes manchitas happy?",
            "question_type": "eleccion simple",
            "options": ["AAAAAAAAAAAAA", "BBBBBBBBBBBBBB"]
        }}

        self.SURVEY_UPDATE = {"description": "I JUST UPDATED THIS SURVEY AAAA"}
            
        

    #######################
    # START EDITION MODE #
    #######################
    """
    UNAUTHORIZED (NOT A SURVEY CREATOR)
    """
    def testUnauthorizedStart(self):
        with self.app as client:
            response = client.post('/surveys/1/edit/start', headers={"Authorization": "Bearer "+self.UNAUTHORIZED_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.NO_PERMISSION["msg"], response.get_data(as_text=True))
      
    """
    UNAUTHORIZED (NOT THE CREATOR OF THE SURVEY)
    """
    def testNotCreatorStart(self):
        with self.app as client:
            response = client.post('/surveys/1/edit/start', headers={"Authorization": "Bearer "+self.DIFFERENT_CREATOR_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.NO_CREATOR["msg"], response.get_data(as_text=True))
    
    """
    CORRECT
    """
    def testCorrectStart(self):
        with self.app as client:
            client.post('/surveys/1/edit/stop', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})
            response = client.post('/surveys/1/edit/start', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(json.loads(response.get_data(as_text=True))["OK"])
    
    """
    REPEAT CORRECT
    """
    def testCorrectStartAgain(self):
        with self.app as client:
            response = client.post('/surveys/1/edit/start', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertFalse(json.loads(response.get_data(as_text=True))["OK"])
    

    #######################
    # STOP EDITION MODE #
    #######################
    """
    UNAUTHORIZED (NOT A SURVEY CREATOR)
    """
    def testUnauthorizedStop(self):
        with self.app as client:
            response = client.post('/surveys/2/edit/stop', headers={"Authorization": "Bearer "+self.UNAUTHORIZED_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.NO_PERMISSION["msg"], response.get_data(as_text=True))
      
    """
    UNAUTHORIZED (NOT THE CREATOR OF THE SURVEY)
    """
    def testNotCreatorStop(self):
        with self.app as client:
            response = client.post('/surveys/2/edit/stop', headers={"Authorization": "Bearer "+self.DIFFERENT_CREATOR_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.NO_CREATOR["msg"], response.get_data(as_text=True))
    
    """
    CORRECT
    """
    def testCorrectStop(self):
        with self.app as client:
            client.post('/surveys/2/edit/start', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})
            response = client.post('/surveys/2/edit/stop', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(json.loads(response.get_data(as_text=True))["OK"])
    
    """
    REPEAT CORRECT
    """
    def testCorrectStopAgain(self):
        with self.app as client:
            response = client.post('/surveys/2/edit/stop', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertFalse(json.loads(response.get_data(as_text=True))["OK"])
    

    #######################
    # UNAUTHORIZE CREATOR #
    #######################
    """
    UNAUTHORIZED (NOT A SURVEY CREATOR)
    """
    def testUnauthorizedUnauthorization(self):
        with self.app as client:
            response = client.delete(f'/surveys/3/edit/del_creator/{self.CREATOR_NAME}', headers={"Authorization": "Bearer "+self.UNAUTHORIZED_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.NO_PERMISSION["msg"], response.get_data(as_text=True))
      
    """
    UNAUTHORIZED (NOT THE CREATOR OF THE SURVEY)
    """
    def testNotCreatorUnauthorization(self):
        with self.app as client:
            response = client.delete(f'/surveys/3/edit/del_creator/{self.CREATOR_NAME}', headers={"Authorization": "Bearer "+self.DIFFERENT_CREATOR_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.NO_CREATOR["msg"], response.get_data(as_text=True))
    
    """
    CORRECT
    """
    def testCorrectUnauthorization(self):
        with self.app as client:
            response = client.delete(f'/surveys/3/edit/del_creator/{self.CREATOR_NAME}', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(json.loads(response.get_data(as_text=True))["OK"])
            client.post(f'/surveys/3/edit/add_creator/{self.CREATOR_NAME}', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})



    #####################
    # AUTHORIZE CREATOR #
    #####################
    """
    UNAUTHORIZED (NOT A SURVEY CREATOR)
    """
    def testUnauthorizedAuthorization(self):
        with self.app as client:
            response = client.post(f'/surveys/3/edit/add_creator/{self.NEW_CREATOR_NAME}', headers={"Authorization": "Bearer "+self.UNAUTHORIZED_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.NO_PERMISSION["msg"], response.get_data(as_text=True))
      
    """
    UNAUTHORIZED (NOT THE CREATOR OF THE SURVEY)
    """
    def testNotCreatorAuthorization(self):
        with self.app as client:
            response = client.post(f'/surveys/3/edit/add_creator/{self.NEW_CREATOR_NAME}', headers={"Authorization": "Bearer "+self.DIFFERENT_CREATOR_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.NO_CREATOR["msg"], response.get_data(as_text=True))
    
    """
    CORRECT
    """
    def testCorrectAuthorization(self):
        with self.app as client:
            response = client.post(f'/surveys/3/edit/add_creator/{self.NEW_CREATOR_NAME}', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})
            self.assertEqual(response.status_code, 200) 
            self.assertTrue(json.loads(response.get_data(as_text=True))["OK"])
            client.delete(f'/surveys/3/edit/del_creator/{self.NEW_CREATOR_NAME}', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})


    ######################
    # DISCONNECT CREATOR #
    ######################
    """
    UNAUTHORIZED (NOT A SURVEY CREATOR)
    """
    def testUnauthorizedDisconnect(self):
        with self.app as client:
            response = client.delete(f'/surveys/1/edit/disconnect', headers={"Authorization": "Bearer "+self.UNAUTHORIZED_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.NO_PERMISSION["msg"], response.get_data(as_text=True))

    """
    CORRECT
    """
    def testCorrectDisconnect(self):
        with self.app as client:            
            response = client.delete(f'/surveys/1/edit/disconnect', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.DISCONNECTED["msg"], response.get_data(as_text=True) )
            self.assertTrue(json.loads(response.get_data(as_text=True))["OK"])
            client.post(f'/surveys/1/edit/connect', headers={"Authorization": "Bearer "+self.UNAUTHORIZED_TOKEN})

    ###################
    # CONNECT CREATOR #
    ###################
    """
    UNAUTHORIZED (NOT A SURVEY CREATOR)
    """
    def testUnauthorizedConnect(self):
        with self.app as client:
            response = client.post(f'/surveys/4/edit/connect', headers={"Authorization": "Bearer "+self.UNAUTHORIZED_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.NO_PERMISSION["msg"], response.get_data(as_text=True))
      
    """
    NOT ALLOWED (The creator hasn't been given access to the edition)
    """
    def testNotAllowedConnect(self):
        with self.app as client:
            response = client.post(f'/surveys/4/edit/connect', headers={"Authorization": "Bearer "+self.DIFFERENT_CREATOR_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.NOT_ALLOWED["msg"], response.get_data(as_text=True))

    """
    CORRECT
    """
    def testCorrectConnect(self):
        with self.app as client:
            response = client.post(f'/surveys/4/edit/connect', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})
            self.assertEqual(response.status_code, 200) 
            self.assertIn(self.CONNECTED["msg"], response.get_data(as_text=True))
            self.assertTrue(json.loads(response.get_data(as_text=True))["OK"])
            client.delete(f'/surveys/4/edit/disconnect', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})


    ################
    # READ UPDATES #
    ################
    
    """
    UNAUTHORIZED (NOT A SURVEY CREATOR)
    """
    def testUnauthorizedGetUpdates(self):
        with self.app as client:
            response = client.get(f'/surveys/1/edit/status', headers={"Authorization": "Bearer "+self.UNAUTHORIZED_TOKEN})
            self.assertEqual(response.status_code, 200) 
            self.assertIn(str(self.NO_PERMISSION["msg"][0]), response.get_data(as_text=True))
            self.assertFalse(json.loads(response.get_data(as_text=True))["OK"])

    """
    NOT ONLINE 
    """
    def testOfflineGetUpdates(self):
        with self.app as client:
            response = client.get(f'/surveys/1/edit/status', headers={"Authorization": "Bearer "+self.DIFFERENT_CREATOR_TOKEN})
            self.assertEqual(response.status_code, 200) 
            self.assertIn(self.NOT_ONLINE["msg"], response.get_data(as_text=True))
            self.assertFalse(json.loads(response.get_data(as_text=True))["OK"])

    """
    CORRECT (BUT NO UPDATES)
    """
    def testCorrectGetNoUpdates(self):
        with self.app as client:
            client.post(f'/surveys/1/edit/connect', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})
            response = client.get(f'/surveys/1/edit/status', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})
            self.assertEqual(response.status_code, 200) 
            self.assertIn(str(self.UPDATES["msg"][0]), response.get_data(as_text=True))
            self.assertTrue(json.loads(response.get_data(as_text=True))["OK"])

    """
    CORRECT
    """
    def testCorrectGetUpdates(self):
        with self.app as client:
            client.post(f'/surveys/1/edit/connect', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})
            response = client.get(f'/surveys/1/edit/status', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN})
            self.assertEqual(response.status_code, 200) 
            self.assertIn(str(self.UPDATES["msg"][0]), response.get_data(as_text=True))
            self.assertTrue(json.loads(response.get_data(as_text=True))["OK"])


    #################
    # UPDATE SURVEY #
    #################

    """
    UNAUTHORIZED (NOT A SURVEY CREATOR)
    """
    def testUnauthorizedUpdateSurvey(self):
        with self.app as client:
            response = client.put(f'/surveys/1/edit/edit_survey', headers={"Authorization": "Bearer "+self.UNAUTHORIZED_TOKEN},json=self.SURVEY_UPDATE)
            self.assertEqual(response.status_code, 200) 
            self.assertIn(str(self.NO_PERMISSION["msg"][0]), response.get_data(as_text=True))
            self.assertFalse(json.loads(response.get_data(as_text=True))["OK"])

    """
    NOT ONLINE 
    """
    def testOfflineUpdateSurvey(self):
        with self.app as client:
            response = client.put(f'/surveys/1/edit/edit_survey', headers={"Authorization": "Bearer "+self.DIFFERENT_CREATOR_TOKEN},json=self.SURVEY_UPDATE)
            self.assertEqual(response.status_code, 200) 
            self.assertIn(self.NOT_ONLINE["msg"], response.get_data(as_text=True))
            self.assertFalse(json.loads(response.get_data(as_text=True))["OK"])

    """
    CORRECT 
    """
    def testCorrectUpdateSurvey(self):
        with self.app as client:
            response = client.put(f'/surveys/1/edit/edit_survey', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN},json=self.SURVEY_UPDATE)
            self.assertEqual(response.status_code, 200) 
            self.assertIn(self.UPDATED["msg"], response.get_data(as_text=True))
            self.assertTrue(json.loads(response.get_data(as_text=True))["OK"])


    ###################
    # UPDATE QUESTION #
    ###################
    
    """
    UNAUTHORIZED (NOT A SURVEY CREATOR)
    """
    def testUnauthorizedUpdateQuestion(self):
        with self.app as client:
            response = client.put(f'/surveys/1/edit/edit_question', headers={"Authorization": "Bearer "+self.UNAUTHORIZED_TOKEN},json=self.QUESTION_UPDATE)
            self.assertEqual(response.status_code, 200) 
            self.assertIn(str(self.NO_PERMISSION["msg"][0]), response.get_data(as_text=True))
            self.assertFalse(json.loads(response.get_data(as_text=True))["OK"])

    """
    NOT ONLINE 
    """
    def testOfflineUpdateQuestion(self):
        with self.app as client:
            response = client.put(f'/surveys/1/edit/edit_question', headers={"Authorization": "Bearer "+self.DIFFERENT_CREATOR_TOKEN},json=self.QUESTION_UPDATE)
            self.assertEqual(response.status_code, 200) 
            self.assertIn(self.NOT_ONLINE["msg"], response.get_data(as_text=True))
            self.assertFalse(json.loads(response.get_data(as_text=True))["OK"])

    """
    CORRECT 
    """
    def testCorrectUpdateQuestion(self):
        with self.app as client:
            response = client.put(f'/surveys/1/edit/edit_question', headers={"Authorization": "Bearer "+self.CREATOR_TOKEN},json=self.QUESTION_UPDATE)
            self.assertEqual(response.status_code, 200) 
            self.assertIn(self.UPDATED["msg"], response.get_data(as_text=True))
            self.assertTrue(json.loads(response.get_data(as_text=True))["OK"])
