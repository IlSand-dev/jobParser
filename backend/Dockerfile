FROM python:3.10 AS base

WORKDIR /usr/src/app


RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt


COPY . .


CMD python manage.py migrate && \
    python manage.py loadcurrency && \
    gunicorn backend.wsgi:application --bind 0.0.0.0:8000

