import unittest
from unittest.mock import patch
import json  # Agregar la importación del módulo json
from db_mongo import MongoDB
from utils import MongoEnum
from app_test import TestAPI
mongo_db = MongoDB()

class TestSurveys(TestAPI):
    
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
