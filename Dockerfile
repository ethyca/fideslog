FROM python:3.9-slim-buster


# Required tools

RUN apt-get update
RUN apt-get install -y \
    g++ \
    gcc


# Update pip and install requirements
RUN pip install -U pip

COPY dev-requirements.txt dev-requirements.txt
RUN pip install -r dev-requirements.txt

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy in the application files and install it locally
COPY . /fideslog
WORKDIR /fideslog
RUN pip install -e .

CMD ["/bin/bash"]
