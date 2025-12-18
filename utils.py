import fitz
import re
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text.lower()


def extract_skills(resume_text, skill_list):
    found = []
    for skill in skill_list:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', resume_text):
            found.append(skill)
    return found


def calculate_ats_score(found_skills, required_skills):
    return round((len(found_skills) / len(required_skills)) * 100, 2)


def calculate_ml_score(resume_text, job_description):
    resume_emb = model.encode(resume_text, convert_to_tensor=True)
    job_emb = model.encode(job_description, convert_to_tensor=True)
    score = util.cos_sim(resume_emb, job_emb)[0][0].item()
    return round(score * 100, 2)
