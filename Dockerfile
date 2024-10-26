FROM python:3.9

RUN apt-get update && \
    apt-get install -y jq && \
    pip install yq pyyaml && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY hello-concourse.py personas.yml /app/
