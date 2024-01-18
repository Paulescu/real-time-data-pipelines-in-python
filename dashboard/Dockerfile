FROM python:3.11.3-slim-buster

# Install build dependencies, including gcc
RUN apt-get update \
    && apt-get install -y gcc \
    && rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND="noninteractive"
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
ENV PYTHONPATH="/app"

WORKDIR /app

# Copy only the requirements file to the container
COPY requirements.txt /app/
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Install hopsworks python library manually here
RUN python3 -m pip install --no-cache-dir "hopsworks==3.4.3"

# Copy the rest of the application code to the container
COPY . /app/
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=80"]