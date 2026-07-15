import unittest
from .scorer import calculate_similarity, score_candidates
from .ner_extractor import extract_skills, extract_experience, extract_education
from .parser import parse_resume
import io
import docx

class TestScorer(unittest.TestCase):
    def test_calculate_similarity_basic(self):
        jd = "We need a Python developer with machine learning experience."
        resume = "I am a software engineer skilled in Python and machine learning."
        
        scores = calculate_similarity(jd, [resume])
        self.assertEqual(len(scores), 1)
        self.assertTrue(scores[0] > 0.0) # Should have some similarity
        
    def test_calculate_similarity_no_match(self):
        jd = "Looking for a React developer."
        resume = "I am a backend engineer working with Java and Spring."
        
        scores = calculate_similarity(jd, [resume])
        self.assertEqual(len(scores), 1)
        self.assertTrue(scores[0] < 0.2) # Should be very low or 0
        
    def test_calculate_similarity_empty(self):
        scores = calculate_similarity("", ["Some resume text"])
        self.assertEqual(scores, [])
        
        scores = calculate_similarity("Some JD", [])
        self.assertEqual(scores, [])
        
    def test_score_candidates(self):
        jd_data = {'text': 'Looking for Python and Django developer', 'skills': ['python', 'django']}
        resumes = [
            {'id': 1, 'text': 'I know python and django very well.', 'skills': ['python', 'django']},
            {'id': 2, 'text': 'I am a java dev.', 'skills': ['java']},
        ]
        
        results = score_candidates(jd_data, resumes)
        self.assertEqual(len(results), 2)
        # Candidate 1 should score higher than Candidate 2
        self.assertTrue(results[0]['candidate_id'] == 1)
        self.assertTrue(results[1]['candidate_id'] == 2)
        self.assertTrue(results[0]['score'] > results[1]['score'])

class TestNERExtractor(unittest.TestCase):
    def test_extract_skills(self):
        text = "I have 5 years of experience in Python, AWS, and Docker."
        skills = extract_skills(text)
        self.assertIn('python', skills)
        self.assertIn('aws', skills)
        self.assertIn('docker', skills)
        
    def test_extract_experience(self):
        text1 = "I have 5 years of experience in software engineering."
        text2 = "Over 10 yrs experience."
        text3 = "No experience mentioned here."
        
        self.assertEqual(extract_experience(text1), 5.0)
        self.assertEqual(extract_experience(text2), 10.0)
        self.assertEqual(extract_experience(text3), 0.0)
        
    def test_extract_education(self):
        self.assertEqual(extract_education("I hold a Ph.D in Computer Science"), "PhD")
        self.assertEqual(extract_education("Bachelor of Science in IT"), "Bachelor")
        self.assertEqual(extract_education("Master's degree in Data Science"), "Master")
        self.assertEqual(extract_education("Some random text without degree"), "Not Specified")

class TestParser(unittest.TestCase):
    def test_parse_resume_unsupported(self):
        with self.assertRaises(ValueError):
            parse_resume(io.BytesIO(b"dummy content"), "resume.txt")
            
    def test_parse_docx_mock(self):
        # Create an in-memory docx
        doc = docx.Document()
        doc.add_paragraph("Hello World. This is a resume.")
        
        f = io.BytesIO()
        doc.save(f)
        f.seek(0)
        
        text = parse_resume(f, "resume.docx")
        self.assertIn("Hello World. This is a resume.", text)

if __name__ == '__main__':
    unittest.main()
