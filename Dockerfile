FROM python:3.11

ENV DB_HOST='localhost'
ENV DB_PORT=5432
ENV DB_NAME='flask_restapi'
ENV DB_USER='flask_restapi'
ENV DB_PASSWORD='flask_restapi_pass'

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
RUN pip install redis
RUN pip install Flask-Session
RUN pip install Werkzeug
RUN pip install Flask-JWT-Extended
RUN pip install DateTime


VOLUME /data_store
EXPOSE 5000

# Command "python3 -m flask run --host=0.0.0.0"
CMD ["poetry", "run", "python3", "-m", "flask", "run", "--host=0.0.0.0"]

