# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /FromDiagram2LaravelAPI
COPY . .

CMD [ "python3", "main.py"]