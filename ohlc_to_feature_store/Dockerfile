FROM python:3.11.3-slim-buster

# Update package list and install build-essential
RUN apt-get update \
    && apt-get install -y build-essential

ENV DEBIAN_FRONTEND="noninteractive"
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

WORKDIR /app
COPY . /app
RUN python3 -m pip install -r requirements.txt
    
# Install hopsworks python library manually here
RUN python3 -m pip install "hopsworks==3.4.3"

ENTRYPOINT ["python3", "src/main.py"]