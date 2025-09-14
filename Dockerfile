# backend/Dockerfile
FROM python:3.11-slim

# install small system deps (helps build wheels and TLS)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy and install python deps first (cached layer)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy application code
COPY . /app

# ensure uploads dir exists
RUN mkdir -p /app/uploads

EXPOSE 8000

# start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
