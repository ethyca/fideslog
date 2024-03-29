FROM python:3.9-slim-bullseye

# Required tools
RUN : \
    && apt-get update \
    && apt-get install -y \
    curl \
    g++ \
    gcc

# Update pip and install requirements
RUN pip install -U pip

COPY dev-requirements.txt dev-requirements.txt
RUN pip install -r dev-requirements.txt

COPY fideslog/api/requirements.txt api-requirements.txt
RUN pip install -r api-requirements.txt

# Copy in the application files and install it locally
COPY . /fideslog
WORKDIR /fideslog
RUN pip install -e .
