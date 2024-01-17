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
COPY . /app
RUN python3 -m pip install -r requirements.txt

# Install hopsworks python library manually here
RUN python3 -m pip install "hopsworks==3.4.3"

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=80"]