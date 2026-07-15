# IntelliScreen AI - Resume Screening Platform

IntelliScreen AI is a production-grade machine learning web application built with Django and PostgreSQL that automates candidate ranking and skill extraction for recruiters.

## Features

- **Authentication System**: Secure recruiter login using Django's built-in authentication
- **Dashboard**: Interactive visualizations of candidate pools using Chart.js
- **Resume Upload**: Batch and individual resume upload supporting PDF and DOCX formats
- **Job Description Parsing**: Automatically extracts required skills and experience from pasted Job Descriptions
- **Candidate Ranking**: Uses TF-IDF and Cosine Similarity to score candidates against a specific job description
- **Skill Matching Display**: Highlights matched skills in green and missing skills in red
- **Background Processing**: Uses Celery and Redis to handle heavy resume parsing asynchronously

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: PostgreSQL
- **Machine Learning**: SpaCy (NER), Scikit-learn (TF-IDF, KMeans), Pandas, NLTK
- **Frontend**: Tailwind CSS, Chart.js, Vanilla HTML/JS
- **Task Queue**: Celery + Redis
- **Containerization**: Docker & Docker Compose

## 🚀 Quick Start (1-Click Run)

The application is completely Dockerized and includes all NLP models, database setup, and message brokers out-of-the-box. 

You can launch the entire stack (PostgreSQL DB, Redis Server, Celery Worker, and Django Web Server) with **a single command**:

```bash
docker-compose up --build
```

**What this command does automatically:**
1. Installs all Python dependencies and heavy ML packages (`spacy`, `scikit-learn`, `pandas`).
2. Downloads the required English NLP models (`en_core_web_sm`, `nltk punkt`).
3. Provisions a local PostgreSQL database and Redis message broker.
4. **Applies all database migrations automatically.**
5. **Creates a default admin superuser** so you can log in immediately.

### Accessing the Application

Once the command finishes building and you see the `web` and `celery` containers running in your terminal:
- Open your browser and navigate to: `http://localhost:8000`
- **Username**: `admin`
- **Password**: `admin`

## Development / Manual Setup

If you wish to run the app natively without Docker (e.g. for development), ensure you have Redis running on your machine, then follow these steps:

1. Create and activate a virtual environment: `python -m venv venv` and `source venv/bin/activate` (or `.\venv\Scripts\Activate.ps1` on Windows)
2. Install requirements: `pip install -r requirements.txt`
3. Download NLP Models:
   - `python -m spacy download en_core_web_sm`
   - `python -m nltk.downloader punkt stopwords punkt_tab`
4. Run migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Start Celery: `celery -A resume_screener worker -l info`
7. Start Server: `python manage.py runserver`

## Testing

To run the unit tests for the ML pipeline natively:
```bash
pytest ml_pipeline/tests.py
```
