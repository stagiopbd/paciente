FROM python:3.6.8-jessie
RUN mkdir /code
ADD . /code/
WORKDIR /code
RUN apt-get update && \
    apt-get -y install curl libssl-dev mysql-client libmysqld-dev libffi-dev locales locales-all nano && \
    pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT gunicorn --workers 4 --reload --timeout 1000 --access-logfile=- --bind 0.0.0.0:8000 api.wsgi