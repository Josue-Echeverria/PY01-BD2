from enum import Enum

class MongoEnum(Enum):
    #For testing
    TEST_ID = 99
    SURVEY_QUESTIONS = [
        {
            "id_question": 1,
            "question_text": " sobre este producto?",
            "question_type": "abierta",
            "response": ""
        },
        {
            "id_question": 2,
            "question_text": "sobre este producto?",
            "question_type": "abierta",
            "response": ""
        }
    ]
    
    @classmethod
    def survey_not_found(cls, id):
        return f"No se encontró el id_survey: {id}"
    
    @classmethod
    def not_added_questions(cls):
        return "No se agregaron nuevas preguntas, todas ya existen en el survey."
    
    @classmethod
    def added_questions(cls, num_questions, id):
        return f"{num_questions} preguntas agregadas al id_survey: {id}"
    
    @classmethod
    def not_found_question(cls, question_id, survey_id):
        return f"No se encontró el question_id: {question_id} en el id_survey: {survey_id}"
    
    @classmethod
    def updated_question(cls, question_id, survey_id):
        return f"Pregunta {question_id} actualizada en el id_survey: {survey_id}"

    @classmethod
    def deleted_question(cls, question_id, survey_id):
        return f"Pregunta {question_id} eliminada del id_survey: {survey_id}"
