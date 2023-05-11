FROM python:latest as development
LABEL authors="Kopanov Anton"

RUN adduser user --disabled-password

WORKDIR /home/user
USER user
RUN mkdir "project"

WORKDIR project
COPY . .

USER root
RUN python setup.py # installing requirements, creating uml and check consistence

USER user
WORKDIR ../
RUN echo "Development image complete"

FROM python:latest as production
COPY --from=development home/user/project/src /src
COPY --from=development home/user/project/data /data
COPY --from=development home/user/project/setup.py setup.py
COPY --from=development home/user/project/requirements.txt requirements.txt
RUN python setup.py --production
RUN rm -f setup.py
RUN rm -f requirements.txt
RUN echo "Production image complete"
ENTRYPOINT python -m src