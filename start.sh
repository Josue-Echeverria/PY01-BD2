#!/bin/bash

# Iniciar el servicio de Flask en segundo plano
poetry run python3 -m flask run --host=0.0.0.0 &

# Iniciar el servicio de Streamlit
streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
