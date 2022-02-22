FROM python:3.10

RUN adduser api

WORKDIR /home/api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN apt-get install -y git gcc g++ tar libffi-dev musl-dev

COPY requirements.txt requirements.txt
RUN python -m venv env

ENV PATH /home/api/env/bin:$PATH

RUN env/bin/pip install -r requirements.txt

COPY api api
COPY user user
COPY manage.py ./

RUN chown -R api:api ./
USER api

EXPOSE 8080
CMD env/bin/gunicorn --bind 0.0.0.0:8080 --access-logfile - --error-logfile - api.wsgi