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
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    && \
    mkdir -p /usr/lib/jvm/java-8-openjdk-amd64 && \
    cd /usr/lib/jvm/java-8-openjdk-amd64 && \
    wget -q https://download.java.net/openjdk/jdk8u41/ri/openjdk-8u41-b04-linux-x64-14_jan_2020.tar.gz && \
    tar xzf openjdk-8u41-b04-linux-x64-14_jan_2020.tar.gz --strip-components=1 && \
    update-alternatives --install /usr/bin/java java /usr/lib/jvm/java-8-openjdk-amd64/bin/java 100 && \
    update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/java-8-openjdk-amd64/bin/javac 100 && \
    rm -rf /var/lib/apt/lists/* && \
    rm openjdk-8u41-b04-linux-x64-14_jan_2020.tar.gz

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64 


RUN pip install kafka-python pymongo streamlit pandas plotly


EXPOSE 5000 8501

# Comando para ejecutar el script de inicio
CMD ["poetry", "run", "python3", "app.py"]
