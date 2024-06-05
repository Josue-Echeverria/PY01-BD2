
import json  # Agregar la importación del módulo json
from db_mongo import MongoDB
from utils import MongoEnum

from app_test import TestAPI


mongo_db = MongoDB()


class TestQuestions(TestAPI):

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
        with self.app as client:
            response = client.put(
                f'/surveys/{MongoEnum.TEST_ID.value}/questions/1')
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 401)
            self.assertIn(self.ERROR_NO_AUTH_HEADERS,
                          response.get_data(as_text=True))

    def testUpdateQuestionNoPermission(self):
        with self.app as client:
            response = client.put(
                '/surveys/1/questions/1', headers={"Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION,
                          response.get_data(as_text=True))

    def testUpdateQuestionNotFoundSurvey(self):
        survey_id = -999
        with self.app as client:
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
        with self.app as client:
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

        with self.app as client:
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
        with self.app as client:
            response = client.delete(
                f'/surveys/{MongoEnum.TEST_ID.value}/questions/1')
            # Verificación de la respuesta
            self.assertEqual(response.status_code, 401)
            self.assertIn(self.ERROR_NO_AUTH_HEADERS,
                          response.get_data(as_text=True))

    def testDeleteQuestionNoPermission(self):
        with self.app as client:
            response = client.delete(
                '/surveys/1/questions/1', headers={"Authorization": f"Bearer {self.ENCUESTADO_TOKEN}"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.ERROR_NO_PERMISSION,
                          response.get_data(as_text=True))

    def testDeleteQuestionNotFoundSurvey(self):
        survey_id = -999
        with self.app as client:
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
        with self.app as client:
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

        with self.app as client:
            # Llamada al endpoint para actualizar la pregunta
            response = client.delete(f'/surveys/{survey_id}/questions/{question_id}', headers={
                                     "Authorization": f"Bearer {self.ADMIN_TOKEN}"})

            self.assertEqual(response.status_code, 200)
            json_response = response.get_json()
            self.assertIn('result', json_response)
            self.assertEqual(json_response['result'], MongoEnum.deleted_question(
                question_id, survey_id))
