import pdfplumber
import docx
import io

def parse_resume(file_obj, filename):
    """
    Parses a resume file (PDF or DOCX) and returns the extracted text.
    file_obj is a file-like object (e.g., from Django's request.FILES)
    """
    ext = filename.lower().split('.')[-1]
    
    text = ""
    
    if ext == 'pdf':
        try:
            with pdfplumber.open(file_obj) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            raise ValueError(f"Failed to parse PDF file: {e}")
            
    elif ext in ['docx', 'doc']:
        try:
            doc = docx.Document(file_obj)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            raise ValueError(f"Failed to parse DOCX file: {e}")
            
    else:
        raise ValueError(f"Unsupported file format: {ext}")
        
    return text.strip()
