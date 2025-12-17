import fitz
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text.lower()


def extract_skills(resume_text, skill_list):
    found_skills = []

    for skill in skill_list:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, resume_text):
            found_skills.append(skill)

    return found_skills


def calculate_skill_score(found_skills, required_skills):
    score = (len(found_skills) / len(required_skills)) * 100
    return round(score, 2)
