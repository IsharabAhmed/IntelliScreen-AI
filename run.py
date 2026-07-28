import os
import sys
import subprocess
from pathlib import Path

# Force UTF-8 stdout encoding for Windows console compatibility
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent

def main():
    print("=" * 60)
    print("[*] Starting IntelliScreen AI - Resume Screening Platform")
    print("=" * 60)

    # 1. Download NLP models if missing
    print("\n[*] Verifying NLP models...")
    try:
        import spacy
        spacy.load("en_core_web_sm")
        print("  [OK] SpaCy en_core_web_sm model loaded.")
    except Exception:
        print("  [>] Downloading SpaCy model 'en_core_web_sm'...")
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"], check=True)

    try:
        import nltk
        nltk.download("punkt", quiet=True)
        nltk.download("stopwords", quiet=True)
        nltk.download("punkt_tab", quiet=True)
        print("  [OK] NLTK datasets verified.")
    except Exception as e:
        print(f"  [!] NLTK download warning: {e}")

    # 2. Database migrations
    print("\n[*] Running database migrations...")
    subprocess.run([sys.executable, "manage.py", "migrate"], cwd=BASE_DIR, check=True)

    # 3. Create default superuser if not exists
    print("\n[*] Checking admin user...")
    create_admin_code = (
        "from accounts.models import User; "
        "User.objects.filter(username='admin').exists() or "
        "(User.objects.create_superuser('admin', 'admin@example.com', 'admin') and print('  [OK] Default admin superuser created.'))"
    )
    subprocess.run([sys.executable, "manage.py", "shell", "-c", create_admin_code], cwd=BASE_DIR, check=True)

    print("\n" + "=" * 60)
    print("[OK] Application ready! Starting development server on http://127.0.0.1:8000")
    print("     Login Credentials -> Username: admin | Password: admin")
    print("=" * 60 + "\n")

    # 4. Start Django server
    subprocess.run([sys.executable, "manage.py", "runserver", "127.0.0.1:8000"], cwd=BASE_DIR)

if __name__ == "__main__":
    main()
