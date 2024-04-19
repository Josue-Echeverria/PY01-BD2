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

    def get_public_surveys(self, start=0, end=None):
        if end is None:
            data = list(self.db.surveys.find({"published": True})[start:])
        else:
            data = list(self.db.surveys.find({"published": True})[start:end])

        return data
    
    def get_survey_detail(self, survey_id):
        survey = self.db.surveys.find_one({"id_survey": int(survey_id)})
        return survey
    
    def update_survey(self, survey_id, updated_data):
        survey_id = int(survey_id)
        
        if not self.db.surveys.find_one({"id_survey": survey_id}):
            return f"No se encontro el id_survey: {survey_id}"
        
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
            return f"No se encontro el id_survey: {survey_id}"

        self.db.surveys.delete_many({"id_survey": survey_id})
        return f"Encuesta eliminada del id_survey: {survey_id}"
    
        
    def show_survey(self, survey_id):
        survey_id = int(survey_id)
        survey = self.db.surveys.find_one({"id_survey": survey_id})
        
        if not survey:
            return f"No se encontro el id_survey: {survey_id}"

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
            return f"No se encontro el id_survey: {survey_id}"

        if not survey.get("published", False):
            return f"La encuesta con id_survey: {survey_id} ya estaba oculta"

        # Actualizar el estado de publicación a False 
        result = self.db.surveys.update_one({"id_survey": survey_id}, {"$set": {"published": False}})
        
        if result.modified_count > 0:
            return f"Encuesta oculta con id_survey: {survey_id}"
        else:
            return f"No se pudo actualizar la encuesta con id_survey: {survey_id}"   



    def get_surveys(self, start=0, end=None):
        # Si end es None, obtén todos los registros a partir del índice de inicio
        if end is None:
            data = list(self.db.surveys.find()[start:])
        else:
            data = list(self.db.surveys.find()[start:end])

        return data
    
    
        
    def get_survey_questions(self, id, start_index, end_index):
        if self.db.surveys.find_one({"id_survey": int(id)}):
            data = self.db.surveys.find_one({"id_survey": int(id)}, {"_id": 0, "questions": 1})
            questions = data.get("questions", [])
            paginated_questions = questions[start_index:end_index]
            return {"questions": paginated_questions}
        else:
            return {"error": MongoEnum.survey_not_found(id)}
                
            
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
        
        if len(answers) == 0:
            return MongoEnum.not_added_answers()
        
        self.db.answers.insert_one({"id_survey": survey_id, "respondent": int(respondent_id), "answers": answers})
        
        return MongoEnum.posted_answers(respondent_id,survey_id)



    def get_answers(self, survey_id, start_index, end_index):
        survey_id = int(survey_id)

        if not self.db.surveys.find_one({"id_survey": survey_id}):
            return {"error": MongoEnum.survey_not_found(survey_id)}

        # Realizar la consulta a la base de datos para obtener las respuestas paginadas
        answers = list(self.db.answers.find({"id_survey": survey_id}, {"_id": 0}).skip(start_index).limit(end_index - start_index))

        return answers



    def get_survey_creator(self, survey_id: int):
        return self.db.surveys.find_one({"id_survey": survey_id}, {"_id": 0, "creator": 1})["creator"]

    def get_survey_analysis(self, survey_id: int):
        analisis = {}
        questions = self.db.surveys.find_one({"id_survey": survey_id}, {"_id": 0, "questions": 1})["questions"]
        
        question_types_in_survey = set()
        for doc in questions:
            question_types_in_survey.add(doc["question_type"])

        if("calificacion" in question_types_in_survey):
            preguntas = list(self.db.surveys.aggregate([
                {'$match': {'id_survey': survey_id}}
                ,{'$project': {'_id': 0, "questions":1 }}
                ,{'$unwind': '$questions'}
                ,{'$match': {'questions.question_type': "calificacion"}}
            ]))

            dict_preguntas = {}
            for pregunta in preguntas: 
                id_pregunta = pregunta["questions"]["id_question"]
                dict_preguntas[id_pregunta] = {}
              
            peores_calificaciones = list(self.db.answers.aggregate([
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
                            , 'id_respondent':{"$first":"$id_respondent"}
                            , 'answer': {"$first":"$answers.answer"}
                            }}
                ]))
            for peor_calificacion in peores_calificaciones:
                dict_preguntas[peor_calificacion["_id"]]["peor_calificacion"] = peor_calificacion

            mejores_calificaciones = list(self.db.answers.aggregate([
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
                            , 'id_respondent':{"$first":"$id_respondent"}
                            , 'answer': {"$first":"$answers.answer"}
                            }}
                ]))
            for mejor_calificacion in mejores_calificaciones:
                dict_preguntas[mejor_calificacion["_id"]]["mejor_calificacion"] = mejor_calificacion

            promedios_calificaciones = list(self.db.answers.aggregate([
                {'$match': {'id_survey': survey_id}} 
                # Se filtran solo la lista de respuestas 
                ,{'$project': {'_id': 0, "id_respondent":0, "id_survey":0}} 
                # Se separan cada elemento en un documento
                ,{'$unwind': '$answers'}
                # Se obtienen las respuestas a las preguntas de tipo calificacion
                ,{'$match': {'answers.question_type': "calificacion"}}
                # Se agrupan y se saca la media por pregunta
                ,{'$group' :{ '_id': '$answers.id_question'
                            , 'average':{'$avg': '$answers.answer'}
                            }}
                ]))
            for promedio_calificacion in promedios_calificaciones:                
                dict_preguntas[promedio_calificacion["_id"]]["promedio_calificacion"] = promedio_calificacion

            analisis["analisis_calificaiones"] = dict_preguntas

        if("numericas" in question_types_in_survey):

            promedio_numericas = list(self.db.answers.aggregate(
                [
                {'$match': {'id_survey': survey_id}} 
                # Se filtran solo la lista de respuestas 
                ,{'$project': {'_id': 0, "id_respondent":0, "id_survey":0}} 
                # Se separan cada elemento en un documento
                ,{'$unwind': '$answers'}
                # Se obtienen las respuestas a las preguntas de tipo calificacion
                ,{'$match': {'answers.question_type': "numericas"}}
                # Se agrupan y se saca la media por pregunta
                ,{'$group' :{ '_id': '$answers.id_question'
                            , 'promedio':{'$avg': '$answers.answer'}
                            }}
                ]))
            
            analisis["analisis_numericas"] = promedio_numericas

        if "si/no" in question_types_in_survey:
            conteo = list(self.db.answers.aggregate([
                {'$match': {'id_survey': survey_id}},
                {'$project': {'_id': 0, "id_respondent":0, "id_survey":0}},  
                {'$unwind': '$answers'},
                {'$match': {'answers.question_type': "si/no"}},
                {'$group': {'_id': '$answers.id_question',
                            'si': {'$sum': {'$cond': [{'$eq': ['$answers.answer', 1]}, 1, 0]}}, 
                            'no': {'$sum': {'$cond': [{'$eq': ['$answers.answer', 0]}, 1, 0]}}   
                            }},
                {'$project': {
                    '_id': 1,
                    'si': 1,
                    'no': 1,
                    'si_%': {'$multiply': [{'$divide': ['$si', {'$add': ['$si', '$no']}]}, 100]},
                    'no_%': {'$multiply': [{'$divide': ['$no', {'$add': ['$si', '$no']}]}, 100]}
                }}
            ]))

            analisis["analisis_si/no"] = conteo
        
        if "eleccion simple" in question_types_in_survey:

            preguntas = list(self.db.surveys.aggregate([
                {'$match': {'id_survey': survey_id}}
                ,{'$project': {'_id': 0, "questions":1 }}
                ,{'$unwind': '$questions'}
                ,{'$match': {'questions.question_type': "eleccion simple"}}
            ]))
            opciones = {}
            for pregunta in preguntas: 
                id_pregunta = pregunta["questions"]["id_question"]
                opciones[id_pregunta] = {}
                for opcion in pregunta["questions"]["options"]:
                    opciones[id_pregunta][opcion] = 0

            respuestas = list(self.db.answers.aggregate([
                {'$match': {'id_survey': survey_id}},
                {"$group": {"_id": None, "total": {"$sum": 1}}}
                ]))[0]
            promedios = list(self.db.answers.aggregate([
                {'$match': {'id_survey': survey_id}},
                {'$project': {'_id': 0, 'id_respondent': 0, 'id_survey': 0}},
                {'$unwind': '$answers'},
                {'$match': {'answers.question_type': "eleccion simple"}}
                ,{"$group": {'_id': "$answers.answer","seleccionada":{"$count":{}}}}#cuenta cuantos encuestados respondieron a
                ,{'$project': {
                    '_id': 1,
                    'seleccionada': {'$multiply': [{'$divide': ['$seleccionada', respuestas["total"]]}, 100]},
                    }}
            ]))

            for key, value in opciones.items():
                for promedio in promedios:
                    if promedio["_id"] in value:
                        value[promedio["_id"]] = promedio["seleccionada"]

            analisis['analisis_eleccion_simple'] = {}
            analisis['analisis_eleccion_simple']["promedios"] = opciones
            analisis['analisis_eleccion_simple']["total_respuestas"] = respuestas["total"]
        
        if "eleccion multiple" in question_types_in_survey:

            preguntas = list(self.db.surveys.aggregate([
                {'$match': {'id_survey': survey_id}}
                ,{'$project': {'_id': 0, "questions":1 }}
                ,{'$unwind': '$questions'}
                ,{'$match': {'questions.question_type': "eleccion multiple"}}
            ]))
            opciones = {}
            for pregunta in preguntas: 
                id_pregunta = pregunta["questions"]["id_question"]
                opciones[id_pregunta] = {}
                for opcion in pregunta["questions"]["options"]:
                    opciones[id_pregunta][opcion] = 0


            respuestas = list(self.db.answers.aggregate([
                {'$match': {'id_survey': survey_id}}
                ,{'$project': {'_id': 0, 'id_respondent': 0, 'id_survey': 0}}
                ,{'$unwind': '$answers'}
                ,{'$match': {'answers.question_type': "eleccion multiple"}}
            ]))
            for respuesta in respuestas:
                actual = respuesta["answers"]
                for opcion_seleccionada in actual["answer"]:
                    opciones[actual["id_question"]][opcion_seleccionada] += 1

            analisis["analisis_eleccion_multiple"] = opciones
          
        return analisis
        