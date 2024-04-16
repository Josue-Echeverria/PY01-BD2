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
    
    
    def post_answers(self, survey_id, respondent_id, answers):
        survey_id = int(survey_id)
        
        if not self.db.surveys.find_one({"id_survey": survey_id}):
            return MongoEnum.survey_not_found(survey_id)
            
        self.db.answers.insert_one({"id_survey": survey_id, "respondent": int(respondent_id), "answers": answers})
        
        return MongoEnum.posted_answers(respondent_id,survey_id)



    def get_answers(self, survey_id):
        survey_id = int(survey_id)
        
        if not self.db.surveys.find_one({"id_survey": survey_id}):
            return MongoEnum.survey_not_found(survey_id)
        
        answers = list(self.db.answers.find({"id_survey": survey_id}, {"_id": 0}))
        
        return answers


    def get_survey_creator(self, survey_id: int):
        return self.db.surveys.find_one({"id_survey": survey_id}, {"_id": 0, "creator": 1})["creator"]

    def get_survey_analysis(self, survey_id: int):
        analisis = {}
        questions = self.get_survey_questions(survey_id)["questions"]
        
        question_types_in_survey = set()
        for doc in questions:
            question_types_in_survey.add(doc["question_type"])

        if("calificacion" in question_types_in_survey):

            peores_calificaciones = list(self.db.answers.aggregate(
                [
                {'$match': {'id_survey': survey_id}} 
                # Se filtran solo la lista de respuestas 
                ,{'$project': {'_id': 0, "id_survey":0}} 
                # Se separan cada elemento en un documento
                ,{'$unwind': '$answers'}
                # Se obtienen las respuestas a las preguntas de tipo calificacion
                ,{'$match': {'answers.question_type': "calificacion"}}

                # Se ordenan las respuesta de forma ascendente
                ,{"$sort":{"answers.answer":1}}
                # Se agrupan las respuestas por id de la pregunta, agarrando el nombre y respuesta del primero que salga
                # (esta de forma ASCENDENTE por lo que sale con el que tiene calificacion mas BAJA)
                ,{'$group' :{ '_id': '$answers.id_question'
                            , 'respondent':{"$first":"$respondent"}
                            , 'answer': {"$first":"$answers.answer"}
                            }}
                ]))

            mejores_calificaciones = list(self.db.answers.aggregate(
                [
                {'$match': {'id_survey': survey_id}} 
                # Se filtran solo la lista de respuestas 
                ,{'$project': {'_id': 0, "id_survey":0}} 
                # Se separan cada elemento en un documento
                ,{'$unwind': '$answers'}
                # Se obtienen las respuestas a las preguntas de tipo calificacion
                ,{'$match': {'answers.question_type': "calificacion"}}
                # Se ordena de forma descendiente
                ,{"$sort":{"answers.answer":-1}}
                # Se agrupan las respuestas por id de la pregunta, agarrando el nombre y respuesta del primero que salga
                # (esta de forma DESCENDIENTE por lo que sale con el que tiene calificacion mas ALTA)
                ,{'$group' :{ '_id': '$answers.id_question'
                            , 'respondent':{"$first":"$respondent"}
                            , 'answer': {"$first":"$answers.answer"}
                            }}
                ]))

            promedio_calificacion = list(self.db.answers.aggregate(
                [
                {'$match': {'id_survey': survey_id}} 
                # Se filtran solo la lista de respuestas 
                ,{'$project': {'_id': 0, "respondent":0, "id_survey":0}} 
                # Se separan cada elemento en un documento
                ,{'$unwind': '$answers'}
                # Se obtienen las respuestas a las preguntas de tipo calificacion
                ,{'$match': {'answers.question_type': "calificacion"}}
                # Se agrupan y se saca la media por pregunta
                ,{'$group' :{ '_id': '$answers.id_question'
                            , 'average':{'$avg': '$answers.answer'}
                            }}
                ]))
            
            analisis["promedio_calificacion"] = promedio_calificacion
            analisis["peores_calificaciones"] = peores_calificaciones
            analisis["mejores_calificaciones"] = mejores_calificaciones

        elif("numericas" in question_types_in_survey):        

            promedio_numericas = list(self.db.answers.aggregate(
                [
                {'$match': {'id_survey': survey_id}} 
                # Se filtran solo la lista de respuestas 
                ,{'$project': {'_id': 0, "respondent":0, "id_survey":0}} 
                # Se separan cada elemento en un documento
                ,{'$unwind': '$answers'}
                # Se obtienen las respuestas a las preguntas de tipo calificacion
                ,{'$match': {'answers.question_type': "numericas"}}
                # Se agrupan y se saca la media por pregunta
                ,{'$group' :{ '_id': '$answers.id_question'
                            , 'average':{'$avg': '$answers.answer'}
                            }}
                ]))
            
            analisis["promedio_numericas"] = promedio_numericas

        return analisis
        
