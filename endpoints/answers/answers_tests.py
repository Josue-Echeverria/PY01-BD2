import unittest
from unittest.mock import patch
import json  # Agregar la importación del módulo json
from db_mongo import MongoDB
from utils import MongoEnum
from app_test import TestAPI
mongo_db = MongoDB()


class TestAnswers(TestAPI):

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
            response = client.get(
                '/surveys/1/analysis', headers={"Authorization": "Bearer "+self.NO_ADMIN_TOKEN})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION,
                          response.get_data(as_text=True))

    def testGetAnalysisSuccesfully(self):
        with self.app as client:
            response = client.get(
                '/surveys/1/analysis', headers={"Authorization": "Bearer "+self.ADMIN_TOKEN})
            self.assertEqual(response.status_code, 200)




