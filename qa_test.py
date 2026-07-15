import os
import requests
import time

BASE_URL = 'http://localhost:8000'
LOGIN_URL = f'{BASE_URL}/accounts/login/'
UPLOAD_URL = f'{BASE_URL}/upload/'
JD_CREATE_URL = f'{BASE_URL}/jd/create/'

def run_tests():
    session = requests.Session()
    
    print("1. Testing Login...")
    # Get CSRF token
    response = session.get(LOGIN_URL)
    if 'csrftoken' in session.cookies:
        csrf_token = session.cookies['csrftoken']
    else:
        print("Failed to get CSRF token.")
        return

    login_data = {
        'username': 'admin',
        'password': 'admin',
        'csrfmiddlewaretoken': csrf_token
    }
    response = session.post(LOGIN_URL, data=login_data, headers={'Referer': LOGIN_URL})
    if response.url == f'{BASE_URL}/' or response.url == f'{BASE_URL}/accounts/profile/':
        print("Login successful.")
    else:
        print(f"Login failed. Redirected to {response.url}")
        return

    print("2. Testing Resume Upload...")
    resumes_dir = 'sample_resumes'
    files_to_upload = []
    
    # Check if dir exists
    if not os.path.exists(resumes_dir):
        print(f"Directory {resumes_dir} does not exist.")
        return
        
    for filename in os.listdir(resumes_dir):
        if filename.endswith('.docx'):
            file_path = os.path.join(resumes_dir, filename)
            files_to_upload.append(('resumes', (filename, open(file_path, 'rb'), 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')))
            
    if not files_to_upload:
        print("No resumes found to upload.")
        return

    response = session.get(UPLOAD_URL)
    csrf_token = session.cookies['csrftoken']
    
    response = session.post(UPLOAD_URL, files=files_to_upload, data={'csrfmiddlewaretoken': csrf_token}, headers={'Referer': UPLOAD_URL})
    print(f"Upload response status: {response.status_code}")
    if response.status_code == 500:
        with open('error_500.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Saved Error 500 Content to error_500.html")
    
    print("Waiting for Celery tasks to process resumes (10 seconds)...")
    time.sleep(10)
    
    print("3. Testing Job Description Creation...")
    response = session.get(JD_CREATE_URL)
    csrf_token = session.cookies['csrftoken']
    jd_data = {
        'title': 'Python Backend Developer',
        'description': 'Looking for a Python Backend Developer with strong skills in Django, Python, REST APIs, and SQL.',
        'csrfmiddlewaretoken': csrf_token
    }
    response = session.post(JD_CREATE_URL, data=jd_data, headers={'Referer': JD_CREATE_URL}, allow_redirects=False)
    print(f"JD Create response status: {response.status_code}")
    if response.status_code == 302:
        redirect_url = response.headers['Location']
        print(f"Successfully created JD. Redirected to {redirect_url}")
        
        # Test JD detail page (which triggers ranking)
        print("4. Testing Candidate Ranking (JD Detail Page)...")
        jd_detail_url = f"{BASE_URL}{redirect_url}"
        response = session.get(jd_detail_url)
        if response.status_code == 200:
            print("Successfully loaded JD detail page.")
            if 'Alice_Smith' in response.text or 'Alice Smith' in response.text:
                print("Candidates appear in the ranking page.")
            else:
                print("Candidates NOT found in ranking page. Either Celery didn't process them or ranking failed.")
        else:
            print(f"Failed to load JD detail page. Status: {response.status_code}")
    else:
        print("Failed to create JD.")

if __name__ == '__main__':
    run_tests()
