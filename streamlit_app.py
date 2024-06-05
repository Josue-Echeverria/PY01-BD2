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

# Filtrar los datos por tipo de pregunta
calificacion_df = df[df['question_type'] == 'calificacion']
si_no_df = df[df['question_type'] == 'si/no']
eleccion_simple_df = df[df['question_type'] == 'eleccion simple']
eleccion_multiple_df = df[df['question_type'] == 'eleccion multiple']

# Visualización interactiva
if not calificacion_df.empty:
    st.write("Preguntas de Calificación")
    calificacion_fig = px.bar(calificacion_df, x='id_question', y='answer', color='id_respondent', title="Calificación por Pregunta")
    st.plotly_chart(calificacion_fig)

if not si_no_df.empty:
    st.write("Preguntas de Sí/No")
    si_no_fig = px.histogram(si_no_df, x='answer', color='id_respondent', title="Respuestas Sí/No")
    st.plotly_chart(si_no_fig)

if not eleccion_simple_df.empty:
    st.write("Preguntas de Elección Simple")
    eleccion_simple_fig = px.pie(eleccion_simple_df, names='answer', title="Distribución de Respuestas de Elección Simple")
    st.plotly_chart(eleccion_simple_fig)

if not eleccion_multiple_df.empty:
    st.write("Preguntas de Elección Múltiple")
    # Desanidar las respuestas de elección múltiple
    multiple_choices = []
    for index, row in eleccion_multiple_df.iterrows():
        for choice in row['answer']:
            multiple_choices.append({
                'id_survey': row['id_survey'],
                'id_respondent': row['id_respondent'],
                'id_question': row['id_question'],
                'choice': choice
            })
    multiple_choices_df = pd.DataFrame(multiple_choices)
    eleccion_multiple_fig = px.histogram(multiple_choices_df, x='choice', title="Distribución de Respuestas de Elección Múltiple")
    st.plotly_chart(eleccion_multiple_fig)

# Actualización automática cada 10 segundos
st.experimental_rerun_interval = 10  # Este es el intervalo de actualización en segundos
time.sleep(st.experimental_rerun_interval)
st.experimental_rerun()
