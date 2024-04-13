from pymongo import MongoClient
import os
from utils import MongoEnum 



config = {
    "host": os.getenv("MONGO_HOST"), 
    "port": int(os.getenv("MONGO_PORT")), 
    "username": os.getenv("MONGO_USER"),
    "password": os.getenv("MONGO_PASSWORD"),
    "database": os.getenv("MONGO_DB")
}



class MongoDB:
    def __init__(self):
        client = MongoClient(
            host=config["host"],
            port=config["port"],
            username=config["username"],
            password=config["password"]
        )
        self.db = client[config["database"]]
        self.db_respuestas = client["db_surveys"]

    
    def get_surveys(self):
        data = list(self.db.surveys.find())
        return data
    
    def get_survey_questions(self, id):
        if self.db.surveys.find_one({"id_survey": int(id)}):
            data = self.db.surveys.find_one({"id_survey": int(id)}, {"_id": 0, "questions": 1})
            return data
        else:
            return {"error":MongoEnum.survey_not_found(id)}
            
        
    def add_questions(self, id, questions):
        id = int(id)
        
        survey = self.db.surveys.find_one({"id_survey": id})
        if not survey:
            return MongoEnum.survey_not_found(id)
        
        # Obtener Ids
        existing_question_ids = [q.get("id_question") for q in survey.get("questions", [])]
        # Filtrar las preguntas nuevas para eliminar las que ya existen en el survey
        questions_to_add = [q for q in questions if q.get("id_question") not in existing_question_ids]
        
        
        # Agregar las preguntas al survey si hay preguntas nuevas por agregar
        if questions_to_add:
            self.db.surveys.update_one(
                {"id_survey": id},
                {"$push": {"questions": {"$each": questions_to_add}}}
            )
            return MongoEnum.added_questions(len(questions_to_add),id)
        else:
            return MongoEnum.not_added_questions()
        
        
    def update_question(self, survey_id, question_id, updated_question):
        survey_id = int(survey_id)
        question_id = int(question_id)
        
        if not self.db.surveys.find_one({"id_survey": survey_id}):
            return MongoEnum.survey_not_found(survey_id)
        
        if not self.db.surveys.find_one({"id_survey": survey_id, "questions.id_question": question_id}):
            return MongoEnum.not_found_question(question_id, survey_id)
        
        # Mantener id de pregunta
        updated_question['id_question'] = question_id
        
        # Actualizar la pregunta
        self.db.surveys.update_one(
            {"id_survey": survey_id, "questions.id_question": question_id},
            { "$set": { f"questions.$": updated_question }}
        )
        
        return MongoEnum.updated_question(question_id, survey_id)

        
    def delete_question(self, survey_id, question_id):
        survey_id = int(survey_id)
        question_id = int(question_id)
        
        
        if not self.db.surveys.find_one({"id_survey": survey_id}):
            return MongoEnum.survey_not_found(survey_id)
        
        if not self.db.surveys.find_one({"id_survey": survey_id, "questions.id_question": question_id}):
            return MongoEnum.not_found_question(question_id, survey_id)
        
        
        self.db.surveys.update_one(
                {"id_survey": survey_id},
                { "$pull": { "questions": { "id_question": question_id } }}
            )
        return MongoEnum.deleted_question(question_id,survey_id)
    

    def get_survey_creator(self, survey_id: int):
        return self.db.surveys.find_one({"id_survey": survey_id}, {"_id": 0, "creator": 1})["creator"]

    def get_survey_analysis(self, survey_id: int):
        print(self.db_respuestas) # AQUI SE TIENEN QUE PROGRAMAR LAS CONSULTAS
