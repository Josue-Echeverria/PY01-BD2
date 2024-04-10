from pymongo import MongoClient
import os 

# Configura los parámetros de conexión
config = {
    "host": os.getenv("MONGO_HOST"), 
    "port": int(os.getenv("MONGO_PORT")), 
    "username": os.getenv("MONGO_USER"),
    "password": os.getenv("MONGO_PASSWORD"),
    "database": os.getenv("MONGO_DB")
}
def test_mongo_connection():
    try:
        # Realiza la conexión a MongoDB
        client = MongoClient(
            host=config["host"],
            port=config["port"],
            username=config["username"],
            password=config["password"]
        )

        # Selecciona la base de datos y la colección
        db = client[config["database"]]
        collection = db["surveys"]

        # Inserta un documento de prueba en la colección
        test_document = {"question": "What is your favorite programming language?", "answer": "Python"}
        result = collection.insert_one(test_document)

        # Recupera el documento insertado
        inserted_doc = collection.find_one({"_id": result.inserted_id})

        # Verifica si la operación fue exitosa
        if inserted_doc:
            print("Conexión a MongoDB exitosa")
            print("Documento insertado:", inserted_doc)
        else:
            print("No se pudo insertar/recuperar datos desde MongoDB")

    except Exception as e:
        print(f"Error de conexión a MongoDB: {str(e)}")

# Ejecuta la función de prueba
test_mongo_connection()
