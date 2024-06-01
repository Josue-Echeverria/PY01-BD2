import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px

# Configurar la conexión con MongoDB
client = MongoClient("mongodb://mongo:27017/")
db = client['db_surveys']
collection = db['answers']

# Recuperar datos de la colección
def get_data():
    data = list(collection.find())
    return pd.DataFrame(data)

# Configurar Streamlit
st.title("Dashboard en Tiempo Real")
st.write("Visualización de datos de encuestas")

# Obtener los datos
data = get_data()

# Mostrar los datos en una tabla
st.write("Datos de las encuestas")
st.dataframe(data)

# Visualización interactiva
fig = px.bar(data, x='campo_x', y='campo_y', title="Gráfico de barras")
st.plotly_chart(fig)
