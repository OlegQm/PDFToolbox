FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wkhtmltopdf \
        ghostscript \
        libxrender1 \
        libfontconfig1 \
        libjpeg62-turbo \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--proxy-headers", \
"--forwarded-allow-ips=*", "--host", "0.0.0.0", \
"--port", "8000", "--reload"]
