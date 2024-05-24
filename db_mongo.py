from pymongo import MongoClient
import os
from utils import MongoEnum 
from datetime import datetime



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
        '''
        Crea una nueva encuesta con los datos proporcionados.
        Parameters:
            data (json): Información de la encuesta a agregar con "name", "description", "id_survey" y "creator"

        Returns:
            questions (json): Un json que contiene la confirmación en el id de creación
            error (str): Un mensaje de error si ya esxiste el id_survey
        '''
        id_survey = data.get("id_survey")
        if self.db.surveys.find_one({"id_survey": id_survey}):
            return f"Ya existe una encuesta con el id_survey: {id_survey}"
        else:
            result = self.db.surveys.insert_one(data)
            self.db.edition_users.insert_one({"id_survey":data["id_survey"], "allowed":[data["creator"]]})
            return result.inserted_id


    def get_public_surveys(self, start=0, end=None):
        '''
        Retorna las encuestas publicadas en la base de datos.

                Parameters:
                        start (int): Tomar elementos desde aquí
                        end (int): Tomar elementos hasta aquí

                Returns:
                        surveys (json): Un json que contiene las encuestas publicas
        '''
        if end is None:
            data = list(self.db.surveys.find({"published": True})[start:])
        else:
            data = list(self.db.surveys.find({"published": True})[start:end])

        return data
    

    def get_survey_detail(self, id_survey):
        '''
        Retorna la información que contiene la encuesta especificada.

                Parameters:
                        start_index (int): Tomar elementos desde aquí
                        end_index (int): Tomar elementos hasta aquí
                        id_survey (int): El id del survey

                Returns:
                        result (json): Un json que contiene la información relacionada al id_survey
        '''        
        survey = self.db.surveys.find_one({"id_survey": int(id_survey)})
        return survey
    

    def update_survey(self, id_survey, updated_data):
        '''
        Actualiza la información de una encuesta especifica.

                Parameters:
                        updated_data (json): información nueva de la encuesta
                        id_survey (int): El id del survey

                Returns:
                        result (json): Un mensaje explicando el resultado de la operación.
                        error (str): Un mensaje de error si no se actualizó la encuesta

        '''         
        id_survey = int(id_survey)
        
        if not self.db.surveys.find_one({"id_survey": id_survey}):
            return f"No se encontro el id_survey: {id_survey}"
        
        update_query = {}
        if "name" in updated_data:
            update_query["name"] = updated_data["name"]
        if "description" in updated_data:
            update_query["description"] = updated_data["description"]       
        if not update_query:
            return "No se proporcionaron campos para actualizar."
        
        result = self.db.surveys.update_one({"id_survey": id_survey}, {"$set": update_query})
        
        if result.modified_count > 0:
            return f"Encuesta actualizada con id_survey: {id_survey}"
        else:
            return f"No se pudo actualizar la encuesta con id_survey: {id_survey}"


    def delete_survey(self, id_survey):
        '''
        Elimina una encuesta especifica.

                Parameters:
                        id_survey (int): El id del survey

                Returns:
                        result (json): Un mensaje explicando el resultado de la operación.
                        error (str): Un mensaje de error si no se encontró la encuesta
        '''           
        id_survey = int(id_survey)
        if not self.db.surveys.find_one({"id_survey": id_survey}):
            return f"No se encontro el id_survey: {id_survey}"

        self.db.surveys.delete_many({"id_survey": id_survey})
        return f"Encuesta eliminada del id_survey: {id_survey}"
    
        
    def  show_survey(self, id_survey):
        '''
        Publica una encuesta modificando su valor "published" a True una encuesta especifica.

                Parameters:
                        id_survey (int): El id del survey

                Returns:
                        result (json): Un mensaje explicando el resultado de la operación.
                        error (str): Un mensaje de error si no se publicó la encuesta
        '''
        id_survey = int(id_survey)
        survey = self.db.surveys.find_one({"id_survey": id_survey})
        
        if not survey:
            return f"No se encontro el id_survey: {id_survey}"

        if survey.get("published", False):
            return f"La encuesta con id_survey: {id_survey} ya estaba publica"

        # Actualizar el estado de publicación a True
        result = self.db.surveys.update_one({"id_survey": id_survey}, {"$set": {"published": True}})
        
        if result.modified_count > 0:
            return f"Encuesta published con id_survey: {id_survey}"
        else:
            return f"No se pudo actualizar la encuesta con id_survey: {id_survey}"
        

    def hide_survey(self, id_survey):
        '''
        Oculta una encuesta modificando su valor "published" a False una encuesta especifica.

                Parameters:
                        id_survey (int): El id del survey

                Returns:
                        result (json): Un mensaje explicando el resultado de la operación.
                        error (str): Un mensaje de error si no se ocultó la encuesta
        '''
        id_survey = int(id_survey)
        survey = self.db.surveys.find_one({"id_survey": id_survey})
        
        if not survey:
            return f"No se encontro el id_survey: {id_survey}"

        if not survey.get("published", False):
            return f"La encuesta con id_survey: {id_survey} ya estaba oculta"

        # Actualizar el estado de publicación a False 
        result = self.db.surveys.update_one({"id_survey": id_survey}, {"$set": {"published": False}})
        
        if result.modified_count > 0:
            return f"Encuesta oculta con id_survey: {id_survey}"
        else:
            return f"No se pudo actualizar la encuesta con id_survey: {id_survey}"   


    def get_surveys(self, start=0, end=None):
        '''
        Retorna todas las encuestas que estén en la base de datos.

                Parameters:
                        start (int): Tomar elementos desde aquí
                        end (int): Tomar elementos hasta aquí

                Returns:
                        result (json): Una colección con las encuestas encontradas.
                        error (str): Un mensaje de error si no se publicó la encuesta
        '''
        # Si end es None, obtén todos los registros a partir del índice de inicio
        if end is None:
            data = list(self.db.surveys.find()[start:])
        else:
            data = list(self.db.surveys.find()[start:end])

        return data
    
        
    def get_survey_questions(self, id, start_index, end_index):
        '''
        Retorna las preguntas relacionadas al id_survey dado encontradas en la base de datos.

                Parameters:
                        start_index (int): Tomar elementos desde aquí
                        end_index (int): Tomar elementos hasta aquí
                        id (int): El id del survey

                Returns:
                        questions (json): Un json que contiene las preguntas relacionadas al id_survey
                        error (str): Un mensaje de error en caso de ocurrir
        '''
        if self.db.surveys.find_one({"id_survey": int(id)}):
            data = self.db.surveys.find_one({"id_survey": int(id)}, {"_id": 0, "questions": 1})
            questions = data.get("questions", [])
            paginated_questions = questions[start_index:end_index]
            return {"questions": paginated_questions}
        else:
            return {"error": MongoEnum.survey_not_found(id)}
                
            
    def add_questions(self, id, questions):
        '''
        Registra las preguntas relacionadas al id_survey en la base de datos.

                Parameters:
                        questions (list): Un array conteniendo las preguntas a agregar
                        id (int): El id del survey
                        
                Returns:
                        result (str): Un mensaje explicando el resultado de la operación
        '''
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
        
        
    def update_question(self, id_survey, question_id, updated_question):
        '''
        Actualiza la pregunta relacionada a ese id_question en el id_survey dado en la base de datos.

                Parameters:
                        updated_question (json): El nuevo cuerpo de la pregunta
                        question_id (int): El id de pregunta
                        id_survey (int): El id del survey

                Returns:
                        result (str): Un mensaje explicando el resultado de la operación
        '''
        id_survey = int(id_survey)
        question_id = int(question_id)
        
        if not self.db.surveys.find_one({"id_survey": id_survey}):
            return MongoEnum.survey_not_found(id_survey)
        
        if not self.db.surveys.find_one({"id_survey": id_survey, "questions.id_question": question_id}):
            return MongoEnum.not_found_question(question_id, id_survey)
        
        # Mantener id de pregunta
        updated_question['id_question'] = question_id
        
        # Actualizar la pregunta
        self.db.surveys.update_one(
            {"id_survey": id_survey, "questions.id_question": question_id},
            { "$set": { f"questions.$": updated_question }}
        )
        
        return MongoEnum.updated_question(question_id, id_survey)

        
    def delete_question(self, id_survey, question_id):
        '''
        Elimina la pregunta relacionada a ese id_question en el id_survey dado en la base de datos.

                Parameters:
                        question_id (int):  El id de pregunta
                        id_survey (int): El id del survey

                Returns:
                        result (str): Un mensaje explicando el resultado de la operación
        '''
        id_survey = int(id_survey)
        question_id = int(question_id)
        
        
        if not self.db.surveys.find_one({"id_survey": id_survey}):
            return MongoEnum.survey_not_found(id_survey)
        
        if not self.db.surveys.find_one({"id_survey": id_survey, "questions.id_question": question_id}):
            return MongoEnum.not_found_question(question_id, id_survey)
        
        
        self.db.surveys.update_one(
                {"id_survey": id_survey},
                { "$pull": { "questions": { "id_question": question_id } }}
            )
        return MongoEnum.deleted_question(question_id,id_survey)
    
    
    def post_answers(self, id_survey, respondent_id, answers):
        '''
        Agrega las respuestas de un encuestado en base relacionadas a una encuesta en la base de datos

                Parameters:
                        respondent_id (int): El id del encuestado
                        answers (list): Un array con todas las respuestas del encuestado
                        id_survey (int): El id del survey

                Returns:
                        result (str): Un mensaje explicando el resultado de la operación
        '''
        id_survey = int(id_survey)
        
        if not self.db.surveys.find_one({"id_survey": id_survey}):
            return MongoEnum.survey_not_found(id_survey)
        
        if len(answers) == 0:
            return MongoEnum.not_added_answers()
        
        self.db.answers.insert_one({"id_survey": id_survey, "respondent": int(respondent_id), "answers": answers})
        
        return MongoEnum.posted_answers(respondent_id,id_survey)


    def get_answers(self, id_survey, start_index, end_index):
        '''
        Retorna todas las respuestas de un survey 

                Parameters:
                        start_index (int): Tomar elementos desde aquí
                        end_index (int): Tomar elementos hasta aquí
                        id_survey (int): El id del survey

                Returns:
                        answers (json): Un json que contiene las respuestas relacionadas al id_survey
        '''
        id_survey = int(id_survey)

        if not self.db.surveys.find_one({"id_survey": id_survey}):
            return {"error": MongoEnum.survey_not_found(id_survey)}

        # Realizar la consulta a la base de datos para obtener las respuestas paginadas
        answers = list(self.db.answers.find({"id_survey": id_survey}, {"_id": 0}).skip(start_index).limit(end_index - start_index))

        return answers


    def get_survey_creator(self, id_survey: int):
        return self.db.surveys.find_one({"id_survey": id_survey}, {"_id": 0, "creator": 1})["creator"]


    def get_survey_analysis(self, id_survey: int):
        analisis = {}
        questions = self.db.surveys.find_one({"id_survey": id_survey}, {"_id": 0, "questions": 1})["questions"]
        
        question_types_in_survey = set()
        for doc in questions:
            question_types_in_survey.add(doc["question_type"])

        if("calificacion" in question_types_in_survey):
            preguntas = list(self.db.surveys.aggregate([
                {'$match': {'id_survey': id_survey}}
                ,{'$project': {'_id': 0, "questions":1 }}
                ,{'$unwind': '$questions'}
                ,{'$match': {'questions.question_type': "calificacion"}}
            ]))

            dict_preguntas = {}
            for pregunta in preguntas: 
                id_pregunta = pregunta["questions"]["id_question"]
                dict_preguntas[id_pregunta] = {}
              
            peores_calificaciones = list(self.db.answers.aggregate([
                {'$match': {'id_survey': id_survey}} 
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
                {'$match': {'id_survey': id_survey}} 
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
                {'$match': {'id_survey': id_survey}} 
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
                {'$match': {'id_survey': id_survey}} 
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
                {'$match': {'id_survey': id_survey}},
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
                {'$match': {'id_survey': id_survey}}
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
                {'$match': {'id_survey': id_survey}},
                {"$group": {"_id": None, "total": {"$sum": 1}}}
                ]))[0]
            promedios = list(self.db.answers.aggregate([
                {'$match': {'id_survey': id_survey}},
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
                {'$match': {'id_survey': id_survey}}
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
                {'$match': {'id_survey': id_survey}}
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
        
    """
    MODO EDICION CON KAFKA
    """
    def start_edition(self, id_survey, user):
        '''
        Cambia el parametro "edition_mode" del survey a true, habilitando la edicion colaborativa

                Parameters:
                        id_survey (int): El id del survey

                Returns:
                        result (json): Un mensaje explicando el resultado de la operación.
                        error (str): Un mensaje de error si no se publicó la encuesta
        '''
        id_survey = int(id_survey)
        survey = self.db.surveys.find_one({"id_survey": id_survey})
        if not survey:
            return {"msg":f"No se encontro el id_survey: {id_survey}", "OK": False}
        if survey["edition_mode"] == True:
            return {"msg":f"La encuesta con id_survey: {id_survey} ya esta en modo edición", "OK": False}

        result = self.db.surveys.update_one({"id_survey": id_survey}, {"$set": {"edition_mode": True}})
        self.register_user_connection(id_survey,user)
        if result.modified_count > 0:
            return {"msg":f"Se ha actualizado el survey con id {id_survey} y ahora esta en modo edicion.", "OK": True}
        else:
            return {"msg":f"No se pudo actualizar la encuesta con id_survey: {id_survey}", "OK": False}
    

    def stop_edition(self, id_survey):
        '''
        Cambia el parametro "edition_mode" del survey a false, habilitando la edicion colaborativa

                Parameters:
                        id_survey (int): El id del survey

                Returns:
                        result (json): Un mensaje explicando el resultado de la operación.
                        error (str): Un mensaje de error si no se publicó la encuesta
        '''
        id_survey = int(id_survey)
        survey = self.db.surveys.find_one({"id_survey": id_survey})
        if not survey:
            return {"msg": f"No se encontro el id_survey: {id_survey}", "OK":False}
        if survey["edition_mode"] == False:
            return {"msg": f"La encuesta con id_survey: {id_survey} no esta en modo edición", "OK":False}
        
        result = self.db.surveys.update_one({"id_survey": id_survey}, {"$set": {"edition_mode": False}})
        self.db.edition_users.update_one({"id_survey": id_survey}, {"$set": {"online": []}})    
        if result.modified_count > 0:
            return {"msg": f"Se ha actualizado el survey con id {id_survey} deteniendo el modo edicion.", "OK":True}
        else:
            return {"msg": f"No se pudo actualizar la encuesta con id_survey: {id_survey}", "OK":False}
        
    
    def register_log(self, id_survey, author, log):
        '''
        Agrega un nuevo mensaje al canal especificado en la base de datos.

        Parameters:
            channel_name (str): Nombre del canal al que se desea agregar el mensaje
            author (str): Nombre del autor del mensaje
            message (str): Contenido del mensaje

        Returns:
            result (str): Un mensaje indicando el éxito de la operación o un error si algo salió mal
        '''
        try:
            message_data = {"author": author, "message": log, "timestamp": datetime.now().strftime("%d de %B a las %H:%M")}
            self.db.channels.update_one({"channel": id_survey}, {"$push": {"messages": message_data}})
            return "Mensaje agregado exitosamente."
        except Exception as e:
            return f"Error al agregar el mensaje: {str(e)}"


    def get_past_logs(self, id_survey):
        '''
        Obtiene todos los mensajes para el canal especificado.

        Parameters:
            id_survey (str): Nombre del canal del que se desean obtener los mensajes

        Returns:
            messages (list): Lista de mensajes para el canal dado
        '''
        logs = self.db.edition_logs.find_one({"id_survey": id_survey}, {"_id": 0, "user": 1, "original":1, "new":1, "msg":1})
        if logs:
            return logs["messages"]
        else:
            return []


    def register_user_connection(self, id_survey, user):
        '''
        Registra la conexion del usuario al modo edicion de la encuesta

        Parameters:
            user (str): nombre del usuario que desea entrar al modo edicion
            id_survey (str): id de la encuesta a la que se desea entrar al modo edicion

        Returns:
            result (str): Un mensaje indicando el éxito de la operación o un error si algo salió mal
        '''
        try:
            result = self.db.edition_users.update_one({"id_survey": id_survey}, {"$push": {"online": user}})
            if result.modified_count == 0:
                return {"msg":"El usuario ya estaba conectado", "OK": False}
            self.db.edition_logs.insert_one({"id_survey": id_survey, "msg": user + " se ha conectado", "date": datetime.now()})
            return {"msg":"Usuario registrado", "OK": True}
        except Exception as e:
            return {"msg":f"Error al agregar el mensaje: {str(e)}", "OK": False}
        

    def register_user_disconnection(self, id_survey, user):
        '''
        Registra la desconexion del usuario al modo edicion de la encuesta

        Parameters:
            user (str): nombre del usuario que desea entrar al modo edicion
            id_survey (str): id de la encuesta a la que se desea entrar al modo edicion

        Returns:
            result (str): Un mensaje indicando el éxito de la operación o un error si algo salió mal
        '''
        try:
            result = self.db.edition_users.update_one({"id_survey": id_survey}, {"$pull": {"online": user}})
            if result.modified_count == 0:
                return {"msg":"El usuario no estaba conectado", "OK": False}
            
            self.db.edition_logs.insert_one({"id_survey": id_survey, "msg": user + " se ha desconectado", "date": datetime.now()})    
            return {"msg":"Usuario desconectado", "OK": True}

        except Exception as e:
            return {"msg":f"Error al agregar el mensaje: {str(e)}", "OK": False}


    def get_allowed(self, id_survey):
        '''
        Obtiene todos los usuarios que estan autorizado a connectarse para la edicion en colaboracion

        Parameters:
            id_survey (str): id de la encuesta que se desea obtnener los usuarios autorizados

        Returns:
            result (array): los nombres de usuarios autorizados a conectarse al modo encuesta. 
        '''
        try:
            result = self.db.edition_users.find_one({"id_survey": id_survey},  {"_id": 0, "allowed": 1})
            return result["allowed"]

        except Exception as e:
            return {"msg":f"Error al obtener los datos : {str(e)}", "OK": False}


    def get_online(self, id_survey):
        '''
        Obtiene todos los usuarios que estan conectados en el modo edicion 

        Parameters:
            id_survey (str): id de la encuesta que se desea obtnener los usuarios conectados

        Returns:
            result (array): los nombres de usuarios conectados al modo edicion de la encuesta
        '''
        try:
            result = self.db.edition_users.find_one({"id_survey": id_survey},  {"_id": 0, "online": 1})
            return result["online"]

        except Exception as e:
            return {"msg":f"Error al obtener los datos : {str(e)}", "OK": False}


    def edit_question(self, user, id_survey, question_id, new_question):
        '''                 
        Edita la pregunta del survey de entrada

        Parameters:
            id_survey (str): id de la encuesta donde se encuentra la pregunta
            question_id (str): id de la pregunta que se desea modificar

        Returns:
            result (array): resultado de la operacion
        '''
        try:
            result = self.db.surveys.find_one_and_update(
                { "id_survey": id_survey}
                ,{ "$set": { "questions.$[question]" :new_question }}
                , array_filters= [ { "question.id_question": question_id }]
                , projection={ "_id":0,'questions': 1 }
                )["questions"]
            original = {}
            for question in result:
                if question["id_question"] == question_id:
                    original = question
                    break
            
            if (original == {}):
                return {"msg":"No se ha encontrado el survey por lo que no se ha modificado la pregunta", "OK": False}
            
            self.db.edition_logs.insert_one({"id_survey": id_survey, "msg": user + " ha modifcado la pregunta " + str(question_id), "date": datetime.now(), "before": original, "after": new_question})
            return {"msg":"Cambios aplicados", "OK": True, "before": original, "after": new_question}
        except Exception as e:
            return {"msg":f"Error al modificar la pregunta: {str(e)}", "OK": False}
        
