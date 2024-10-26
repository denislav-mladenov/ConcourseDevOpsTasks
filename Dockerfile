# Start with the base Python image
FROM python:3.9

# Install yq and jq
RUN apt-get update && \
    apt-get install -y jq && \
    pip install yq && \
    rm -rf /var/lib/apt/lists/*

# Set a working directory
WORKDIR /app

