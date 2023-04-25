FROM python:latest
LABEL authors="Kopanov Anton"

RUN adduser user --disabled-password
WORKDIR /home/user
USER user
RUN mkdir "project"
WORKDIR project
COPY /src src
COPY /uml uml
COPY README.md README.md
COPY requirements.txt requirements.txt
COPY setup.py setup.py
COPY static_analyze static_analyze
COPY tests tests
COPY /data data
USER root
RUN python setup.py
RUN rm setup.py
USER user
WORKDIR ../