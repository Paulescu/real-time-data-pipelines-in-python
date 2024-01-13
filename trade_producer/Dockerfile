FROM python:3.11.3-slim-buster

ENV DEBIAN_FRONTEND="noninteractive"
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
ENV PYTHONPATH="/app"

WORKDIR /app
COPY . /app
RUN python3 -m pip install -r requirements.txt

# ENTRYPOINT ["python3", "src/main.py", "--use_local_kafka=true"]
ENTRYPOINT ["python3", "src/main.py"]