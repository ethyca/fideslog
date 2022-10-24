FROM python:3.9-slim-bullseye

# Required tools
RUN apt-get update
RUN apt-get install -y curl g++ gcc

# Update pip and install requirements
RUN pip install -U pip

COPY dev-requirements.txt dev-requirements.txt
RUN pip install -r dev-requirements.txt

COPY fideslog/api/requirements.txt api-requirements.txt
RUN pip install -r api-requirements.txt

COPY /api /api/
COPY fideslog.toml /api
COPY fideslog.env /api
WORKDIR /api/
RUN pip install -e /api/