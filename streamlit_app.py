import os
import time
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

# Función para obtener y normalizar los datos de MongoDB
def get_data():
    data_from_mongodb = list(collection.find())
    normalized_data = normalize_answers(data_from_mongodb)
    df = pd.DataFrame(normalized_data)
    return df

# Configurar Streamlit
st.title("Dashboard en Tiempo Real")
st.write("Visualización de datos de encuestas")

# Obtener y mostrar los datos
df = get_data()

# Mostrar los datos en una tabla
st.write("Datos de las encuestas")
st.dataframe(df)

# Visualización interactiva (ejemplo de gráfico de barras)
fig = px.bar(df, x='id_question', y='answer', color='question_type', title="Respuestas por Pregunta")
st.plotly_chart(fig)

# Actualización automática cada 10 segundos
st.experimental_rerun_interval = 10  # Este es el intervalo de actualización en segundos
time.sleep(st.experimental_rerun_interval)
st.experimental_rerun()
