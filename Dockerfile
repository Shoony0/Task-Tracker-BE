FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app/src

WORKDIR /app/src/

# Install system dependencies required to build mysqlclient
RUN apt-get update \
    && apt-get install -y gcc python3-dev default-libmysqlclient-dev build-essential pkg-config \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /app/src/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/src/

RUN ls -la

RUN chmod +x /app/src/setup.sh
ENTRYPOINT ["/app/src/setup.sh"]

# docker build -t my-django-app .
# docker compose --env-file .env  up --build
# docker compose --env-file .env exec web bash