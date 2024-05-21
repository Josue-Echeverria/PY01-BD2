import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px

# Conectar a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["nombre_de_tu_base_de_datos"]
collection = db["nombre_de_tu_coleccion"]

# Leer datos de MongoDB
data = list(collection.find())
df = pd.DataFrame(data)

# Crear una visualización
fig = px.bar(df, x='campo_de_pregunta', y='campo_de_respuesta')

# Mostrar la visualización en Streamlit
st.plotly_chart(fig)

# Configurar recarga automática (esto puede ser mejorado con técnicas más avanzadas como websockets)
if st.button('Actualizar'):
    st.experimental_rerun()
