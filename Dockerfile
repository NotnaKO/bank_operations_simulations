FROM python:latest
LABEL authors="Kopanov Anton"

RUN adduser user --disabled-password

WORKDIR /home/user
USER user
RUN mkdir "project"

WORKDIR project
COPY ./ ./

USER root
RUN python setup.py

USER user
WORKDIR ../