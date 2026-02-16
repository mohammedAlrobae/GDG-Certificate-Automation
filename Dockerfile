FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for Pillow and other potential needs
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    libfreetype6-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
