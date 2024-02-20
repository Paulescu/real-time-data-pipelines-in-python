# FROM python:3.11.3-slim-buster

# ENV DEBIAN_FRONTEND="noninteractive"
# ENV PYTHONUNBUFFERED=1
# ENV PYTHONIOENCODING=UTF-8
# ENV PYTHONPATH="/app"

# WORKDIR /app
# COPY . /app
# RUN python3 -m pip install -r requirements.txt

# ENTRYPOINT ["python3", "src/main.py"]

FROM python:3.10.3-slim-buster

ENV DEBIAN_FRONTEND="noninteractive"
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
ENV PYTHONPATH="/app"

# Set the working directory to /app
WORKDIR /app

# Copy only the requirements file to the container and install dependencies
COPY requirements.txt /app/

# Install the dependencies
# RUN python3 -m pip install --no-cache-dir -r requirements.txt
RUN find | grep requirements.txt | xargs -I '{}' python3 -m pip install -r '{}' --extra-index-url https://pkgs.dev.azure.com/quix-analytics/53f7fe95-59fe-4307-b479-2473b96de6d1/_packaging/public/pypi/simple/

# Copy the rest of the application code to the container
COPY . /app

ENTRYPOINT ["python3", "src/main.py"]