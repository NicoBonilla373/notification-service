FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema (a veces necesarias para pip)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["python", "app.py"]

