FROM mirror.gcr.io/python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry install

COPY source entrypoint.sh ./

RUN chmod 777 entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
