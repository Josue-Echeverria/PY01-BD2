from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession, SQLContext, Row
from pymongo import MongoClient
from datetime import datetime, date
import time
import os 
import pyspark

def normalize_answers(data):
    records = []
    for entry in data:
        for answer in entry['answers']:
            record = {
                'id_survey': entry['id_survey'],
                'id_respondent': entry['id_respondent'],
                'id_question': answer['id_question'],
                'answer': answer['answer'],
                'question_type': answer['question_type']
            }
            records.append(record)
    return records

def read_from_mongodb(collection_name):
    try:
        config = {
            "host": os.getenv("MONGO_HOST"), 
            "port": int(os.getenv("MONGO_PORT")), 
            "username": os.getenv("MONGO_USER"),
            "password": os.getenv("MONGO_PASSWORD"),
            "database": os.getenv("MONGO_DB")
        }

        client = MongoClient(
            host=config["host"],
            port=config["port"],
            username=config["username"],
            password=config["password"]
        )
        db = client[config["database"]]
        collection = db[collection_name]
        data_from_mongodb = list(collection.find())

        print(f"Lectura de datos desde la colección '{collection_name}':")
        # for document in data_from_mongodb:
        #     print(document)
        
        # Obtener datos normalizados
        normalized_data = normalize_answers(data_from_mongodb)
        print(normalized_data)

        # Crear RDD a partir de los datos normalizados
        rdd = sc.parallelize(normalized_data)

        surveys = sqlC.createDataFrame(rdd)
            
        print("Contenido del RDD:")
        for record in rdd.collect():
            print(record)
        
        #surveys.show() 
        time.sleep(20)

    except Exception as e:
        print(f"ERROR '{collection_name}': {str(e)}")


def prueba_config():
    try:
        # conf = pyspark.SparkConf()\
        # .setMaster("spark://spark-master:7077")

            # # Configuración de Spark
        SPARK_MASTER = "spark://localhost:7077" # "spark://localhost:7077" asi y corriendo py spark.py funciona bien
        spark = SparkConf().setAppName("Lectura de datos desde MongoDB SURVEYS").setMaster(SPARK_MASTER)
        
        # spark = SparkSession \
        #     .builder \
        #     .appName("Lectura de datos desde MongoDB") \
        #     .config(conf=conf) \
        #     .getOrCreate()
        
        sc = SparkContext(conf=spark)
        # Generar datos de ejemplo
        data = list(range(1, 6))

        # Crear un RDD a partir de los datos
        my_rdd = sc.parallelize(data)

        # Contar el total de elementos en el RDD
        total_elements = my_rdd.count()
        print(f"Total elements in RDD: {total_elements}")

        # Obtener el número predeterminado de particiones
        num_partitions = my_rdd.getNumPartitions()
        print(f"Default number of partitions: {num_partitions}")

        # Calcular el máximo, mínimo y suma de los elementos en el RDD
        max_value = my_rdd.max()
        min_value = my_rdd.min()
        sum_value = my_rdd.sum()
        print("holaaaa")
        print(f"MAX~>{max_value}, MIN~>{min_value}, SUM~>{sum_value}")

    except Exception as e:
        print(f"An error occurred: {str(e)}") 
        
if __name__ == "__main__":
    # configuracion de Spark
    try:
        conf = pyspark.SparkConf()
        conf.set("spark.driver.memory", "11g")
        conf.setMaster("spark://spark-master:7077")

        spark = SparkSession.builder \
            .appName("Lectura de datos desde MongoDB") \
            .config(conf=conf)\
            .getOrCreate()

        sc = spark.sparkContext
        sqlC = SQLContext(sc)
        # prueba_config()
        read_from_mongodb("answers")

    except Exception as e:
        print(f"ERROR: {str(e)}")