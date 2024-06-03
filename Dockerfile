FROM python:3.11

ENV DB_HOST='localhost'
ENV DB_PORT=5432
ENV DB_NAME='flask_restapi'
ENV DB_USER='flask_restapi'
ENV DB_PASSWORD='flask_restapi_pass'

ENV KAFKA_BROKER1='kafka:9092'
ENV KAFKA_CONSUMER_OFFSET_SECONDS=30

ENV REDIS_HOST='redis-master'
ENV REDIS_PORT=6379
ENV REDIS_DB=0

ENV JWT_SECRET_KEY='butthecoffeeinperuismuchhotter'
ENV APP_SECRET_KEY='mandatoryfunactivities'


WORKDIR /opt/app

COPY . .

RUN pip install poetry
RUN poetry lock --no-update
RUN poetry install

RUN pip install kafka-python pymongo streamlit pandas plotly


EXPOSE 5000 8501

# Comando para ejecutar el script de inicio
CMD ["poetry", "run", "python3", "app.py"]
