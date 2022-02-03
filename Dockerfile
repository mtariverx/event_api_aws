FROM python:latest

COPY requirements.txt wsgi.py ./
COPY app /app

RUN pip install -r requirements.txt

