import os
from flask import Blueprint, jsonify
from pymongo import MongoClient
from neo4j import GraphDatabase
from app_service import AppService
from db import Database

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


db = Database(database=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)
appService = AppService(db)

# Configuración de MongoDB
config_mongo = {
    "host": os.getenv("MONGO_HOST"), 
    "port": int(os.getenv("MONGO_PORT")), 
    "username": os.getenv("MONGO_USER"),
    "password": os.getenv("MONGO_PASSWORD"),
    "database": os.getenv("MONGO_DB")
}

# Configuración de Neo4j
config_neo4j = {
    "uri":  os.getenv("NEO4J_URI"),
    "user": os.getenv("NEO_USER"),
    "password":  os.getenv("NEO_PASS")
}

class MongoDB:
    def __init__(self):
        client = MongoClient(
            host=config_mongo["host"],
            port=config_mongo["port"],
            username=config_mongo["username"],
            password=config_mongo["password"]
        )
        self.db = client[config_mongo["database"]]

    def get_all_answers(self):
        '''
        Retorna todas las respuestas de todas las encuestas

                Returns:
                        answers (json): Un json que contiene todas las respuestas
        '''
        answers = list(self.db.answers.find({}, {"_id": 0}))
        for answer in answers:
            id_survey = answer['id_survey']
            id_respondent = answer['id_respondent']
            survey = self.db.surveys.find_one({"id_survey": id_survey}, {"_id": 0, "name": 1})
            respondents = appService.get_respondents_by_id(id_respondent)
            answer['survey_name'] = survey['name']
            if respondents and len(respondents[0]) > 2:
                answer['respondent_name'] = respondents[0][2]
            else:
                answer['respondent_name'] = 'Desconocido'

        return answers





class Neo4jDB:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            config_neo4j["uri"], 
            auth=(config_neo4j["user"], config_neo4j["password"])
        )

    def close(self):
        self.driver.close()




    def create_survey_node_and_associate_respondents(self, responses):
        with self.driver.session() as session:
            session.write_transaction(self._create_survey_node_and_associate_respondents_tx, responses)

    @staticmethod
    def _create_survey_node_and_associate_respondents_tx(tx, responses):
        # Limpia el grafo anterior
        tx.run("MATCH (survey:Survey) DETACH DELETE survey")
        tx.run("MATCH (respondent:Respondent) DETACH DELETE respondent")

        # Se crean los nodos y las relaciones
        for response in responses:
            survey_name = response['survey_name']
            survey_id = response['id_survey']
            respondent_id = str(response['id_respondent'])
            respondent_name = response['respondent_name']
            answers = response['answers']
            # Crea el nodo survey 
            tx.run("MERGE (survey:Survey {name: $survey_name, survey_id: $survey_id})", survey_name=survey_name, survey_id=survey_id)
            # Crea el nodo respondent
            tx.run("MERGE (respondent:Respondent {id_respondent: $respondent_id, name: $respondent_name})", respondent_id=respondent_id, respondent_name=respondent_name)
            # asocia respondent con survey
            tx.run("""
                MATCH (survey:Survey {name: $survey_name, survey_id: $survey_id}), (respondent:Respondent {id_respondent: $respondent_id})
                CREATE (respondent)-[:RESPONDED_TO]->(survey)
            """, survey_name=survey_name, survey_id=survey_id, respondent_id=respondent_id)

        # Calcula la similitud entre respuestas
        surveys = {}
        for response in responses:
            survey_name = response['survey_name']
            if survey_name not in surveys:
                surveys[survey_name] = []
            surveys[survey_name].append(response)

        for survey_name, survey_responses in surveys.items():
            for i, response1 in enumerate(survey_responses):
                for j, response2 in enumerate(survey_responses):
                    if i < j:  # Para evitar duplicados, solo comparar una vez (i < j)
                        similarity_score = Neo4jDB._calculate_similarity(response1['answers'], response2['answers'])
                        if similarity_score > 0:
                            respondent1_id = str(response1['id_respondent'])
                            respondent2_id = str(response2['id_respondent'])
                            tx.run("""
                                MATCH (respondent1:Respondent {id_respondent: $respondent1_id}), (respondent2:Respondent {id_respondent: $respondent2_id})
                                MERGE (respondent1)-[s:SIMILAR_TO]-(respondent2)
                                ON CREATE SET s.weight = $similarity_score
                                ON MATCH SET s.weight = s.weight + $similarity_score
                            """, respondent1_id=respondent1_id, respondent2_id=respondent2_id, similarity_score=similarity_score)

    @staticmethod
    def _calculate_similarity(answers1, answers2):
        similarity_score = 0
        for answer1 in answers1:
            for answer2 in answers2:
                if answer1['id_question'] == answer2['id_question'] and answer1['answer'] == answer2['answer']:
                    similarity_score += 1
        return similarity_score


# Crear instancias de MongoDB y Neo4jDB
mongo_db = MongoDB()

# Crear el blueprint
neo4j_app = Blueprint('neo4j_app', __name__)

@neo4j_app.route("/surveys/graph", methods=["GET"])
def create_graph():
    responses = mongo_db.get_all_answers()
    neo4j_db = Neo4jDB()  
    neo4j_db.create_survey_node_and_associate_respondents(responses)
    neo4j_db.close() 
    return jsonify({"message": "Grafo creado correctamente http://localhost:7474/ "}), 200



@neo4j_app.route("/surveys/resp", methods=["GET"])
def get_all_survey_responses():
    responses = mongo_db.get_all_answers()
    return jsonify({"responses": responses})