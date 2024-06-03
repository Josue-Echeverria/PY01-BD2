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

# Convertir los datos a un DataFrame de pandas
df = pd.DataFrame(data_from_mongodb)

# Función para asegurar que los valores en 'answers' sean listas
def ensure_list(x):
    if isinstance(x, list):
        return x
    elif pd.isnull(x):
        return []
    else:
        return [x]

# Aplicar la función a la columna 'answers'
if 'answers' in df.columns:
    df['answers'] = df['answers'].apply(ensure_list)

# Configurar Streamlit
st.title("Dashboard en Tiempo Real")
st.write("Visualización de datos de encuestas")

# Mostrar los datos en una tabla
st.write("Datos de las encuestas")
st.dataframe(df)

# Verificar la existencia de 'campo_x' y 'campo_y' antes de crear el gráfico
if 'campo_x' in df.columns and 'campo_y' in df.columns:
    # Visualización interactiva con Plotly
    fig = px.bar(df, x='campo_x', y='campo_y', title="Gráfico de barras")
    st.plotly_chart(fig)
else:
    st.write("Las columnas 'campo_x' y 'campo_y' no existen en el DataFrame.")
