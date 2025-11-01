## take the base image
FROM python:3.11-slim

## set the working directory
WORKDIR /app

## install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

## copy the requirements file
COPY requirements.txt .

## install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

## copy the rest of the files
COPY app/ ./app/

## expose the port
EXPOSE 8001

## run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
