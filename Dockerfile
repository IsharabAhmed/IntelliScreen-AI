# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Download NLP models
RUN python -m spacy download en_core_web_sm
RUN python -m nltk.downloader punkt stopwords punkt_tab

# Copy project
COPY . /app/

# Collect static files (optional, handled in entrypoint or docker-compose usually, but good for pure prod images)
# RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD ["gunicorn", "resume_screener.wsgi:application", "--bind", "0.0.0.0:8000"]
