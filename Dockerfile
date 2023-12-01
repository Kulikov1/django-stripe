FROM python:3.11.4-slim-buster
RUN mkdir /app
WORKDIR /app
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .