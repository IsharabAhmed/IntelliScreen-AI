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

## 🚀 Quick Start (Single-Command Run - No Docker Needed)

You can launch the complete application with **a single command** without Docker, Redis, or PostgreSQL dependencies:

```bash
python run.py
```
*(On Windows, you can also double-click or run `run.bat`; on Linux/macOS, `./run.sh`)*

**What this single command does automatically:**
1. Verifies and downloads required NLP models (`spacy en_core_web_sm` and NLTK packages).
2. Applies all database migrations automatically (`SQLite`).
3. Ensures a default admin user is ready (`admin` / `admin`).
4. Configures background parsing to run synchronously (`CELERY_TASK_ALWAYS_EAGER`).
5. Starts the web server on `http://127.0.0.1:8000`.

### Accessing the Application

Once started, open your web browser to:
- **URL**: `http://localhost:8000`
- **Username**: `admin`
- **Password**: `admin`

## Docker Setup (Optional)

If you prefer to run with Docker Compose:
```bash
docker-compose up --build
```


## Testing

To run the unit tests for the ML pipeline natively:
```bash
pytest ml_pipeline/tests.py
```
