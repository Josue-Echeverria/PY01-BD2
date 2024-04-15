from pymongo import MongoClient
import os


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

    def add_survey(self, data):
        survey_id = data.get("id_survey")
        if self.db.surveys.find_one({"id_survey": survey_id}):
            return f"Ya existe una encuesta con el id_survey: {survey_id}"
        else:
            result = self.db.surveys.insert_one(data)
            return result.inserted_id

    def get_public_surveys(self):
        data = list(self.db.surveys.find({"published": True}))
        return data
    
    def get_survey_detail(self, survey_id):
        survey = self.db.surveys.find_one({"id_survey": int(survey_id)})
        return survey
    
    def update_survey(self, survey_id, updated_data):
        survey_id = int(survey_id)
        
        if not self.db.surveys.find_one({"id_survey": survey_id}):
            return f"No se encontró el id_survey: {survey_id}"
        
        update_query = {}
        if "name" in updated_data:
            update_query["name"] = updated_data["name"]
        if "description" in updated_data:
            update_query["description"] = updated_data["description"]       
        if not update_query:
            return "No se proporcionaron campos para actualizar."
        
        result = self.db.surveys.update_one({"id_survey": survey_id}, {"$set": update_query})
        
        if result.modified_count > 0:
            return f"Encuesta actualizada con id_survey: {survey_id}"
        else:
            return f"No se pudo actualizar la encuesta con id_survey: {survey_id}"


    def delete_survey(self, survey_id):
        survey_id = int(survey_id)
        if not self.db.surveys.find_one({"id_survey": survey_id}):
            return f"No se encontró el id_survey: {survey_id}"

        self.db.surveys.delete_many({"id_survey": survey_id})
        return f"Encuesta eliminada del id_survey: {survey_id}"
    
        
    def show_survey(self, survey_id):
        survey_id = int(survey_id)
        survey = self.db.surveys.find_one({"id_survey": survey_id})
        
        if not survey:
            return f"No se encontró el id_survey: {survey_id}"

        if survey.get("published", False):
            return f"La encuesta con id_survey: {survey_id} ya estaba publica"

        # Actualizar el estado de publicación a True
        result = self.db.surveys.update_one({"id_survey": survey_id}, {"$set": {"published": True}})
        
        if result.modified_count > 0:
            return f"Encuesta published con id_survey: {survey_id}"
        else:
            return f"No se pudo actualizar la encuesta con id_survey: {survey_id}"
        
    def hide_survey(self, survey_id):
        survey_id = int(survey_id)
        survey = self.db.surveys.find_one({"id_survey": survey_id})
        
        if not survey:
            return f"No se encontró el id_survey: {survey_id}"

        if not survey.get("published", False):
            return f"La encuesta con id_survey: {survey_id} ya estaba oculta"

        # Actualizar el estado de publicación a False 
        result = self.db.surveys.update_one({"id_survey": survey_id}, {"$set": {"published": False}})
        
        if result.modified_count > 0:
            return f"Encuesta oculta con id_survey: {survey_id}"
        else:
            return f"No se pudo actualizar la encuesta con id_survey: {survey_id}"   
    
    def get_surveys(self):
        data = list(self.db.surveys.find())
        return data
    
    def get_survey_questions(self, id):
        if self.db.surveys.find_one({"id_survey": int(id)}):
            data = self.db.surveys.find_one({"id_survey": int(id)}, {"_id": 0, "questions": 1})
            return data
        else:
            return f"No se encontró el id_survey: {id}"
            
        
    def add_questions(self, id, questions):
        id = int(id)
        
        survey = self.db.surveys.find_one({"id_survey": id})
        if not survey:
            return f"No se encontró el id_survey: {id}"
        
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
            return f"{len(questions_to_add)} preguntas agregadas al id_survey: {id}"
        else:
            return "No se agregaron nuevas preguntas, todas ya existen en el survey."

        
        
    def update_question(self, survey_id, question_id, updated_question):
        survey_id = int(survey_id)
        question_id = int(question_id)
        
        if not self.db.surveys.find_one({"id_survey": survey_id}):
            return f"No se encontró el id_survey: {survey_id}"
        
        if not self.db.surveys.find_one({"id_survey": survey_id, "questions.id_question": question_id}):
            return f"No se encontró el question_id: {question_id} en el id_survey: {survey_id}"
        
        # Mantener id de pregunta
        updated_question['id_question'] = question_id
        
        # Actualizar la pregunta
        self.db.surveys.update_one(
            {"id_survey": survey_id, "questions.id_question": question_id},
            { "$set": { f"questions.$": updated_question }}
        )
        
        return f"Pregunta {question_id} actualizada en el id_survey: {survey_id}"

        
    def delete_question(self, survey_id, question_id):
        survey_id = int(survey_id)
        question_id = int(question_id)
        
        
        if not self.db.surveys.find_one({"id_survey": survey_id}):
            return f"No se encontró el id_survey: {survey_id}"
        
        if not self.db.surveys.find_one({"id_survey": survey_id, "questions.id_question": question_id}):
            return f"No se encontró el question_id: {question_id} en el id_survey: {survey_id}"
        
        self.db.surveys.update_one(
                {"id_survey": survey_id},
                { "$pull": { "questions": { "id_question": question_id } }}
            )
        return f"Pregunta {question_id} eliminada del id_survey: {survey_id}"
