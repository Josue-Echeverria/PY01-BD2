import os
import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px

# Configuración de conexión a MongoDB
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
collection = db["answers"]
data_from_mongodb = list(collection.find())

# Desanidar los datos de la colección 'answers'
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

# Normalizar los datos
normalized_data = normalize_answers(data_from_mongodb)

# Convertir los datos normalizados a un DataFrame de Pandas
df = pd.DataFrame(normalized_data)

# Configurar Streamlit
st.title("Dashboard en Tiempo Real")
st.write("Visualización de datos de encuestas")

# Mostrar los datos en una tabla
st.write("Datos de las encuestas")
st.dataframe(df)

# Visualización interactiva (ejemplo de gráfico de barras)
fig = px.bar(df, x='id_question', y='answer', color='question_type', title="Respuestas por Pregunta")
st.plotly_chart(fig)
