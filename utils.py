import re
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------- CLEAN TEXT ----------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text


# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text_from_pdf(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


# ---------------- SKILL SCORE ----------------
def calculate_skill_score(resume_text, must_have_skills, optional_skills):
    resume_text = clean_text(resume_text)

    must_matched = 0
    optional_matched = 0

    for skill in must_have_skills:
        if skill in resume_text:
            must_matched += 1

    for skill in optional_skills:
        if skill in resume_text:
            optional_matched += 1

    must_score = (must_matched / len(must_have_skills)) * 100 if must_have_skills else 0
    optional_score = (optional_matched / len(optional_skills)) * 100 if optional_skills else 0

    # Must-have skills dominate
    final_skill_score = (0.80 * must_score) + (0.20 * optional_score)

    return round(final_skill_score, 2)


# ---------------- TF-IDF SIMILARITY ----------------
def tfidf_similarity(role_text, resume_text):
    corpus = [
        clean_text(role_text),
        clean_text(resume_text)
    ]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(corpus)

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity * 100, 2)


# ---------------- NORMALIZE TF-IDF ----------------
def normalize_tfidf(score):
    return max(40, score)  # prevents unfair low scores


# ---------------- ATS SCORE ----------------
def calculate_ats_score(resume_text, job_requirements):
    skill_score = calculate_skill_score(
        resume_text,
        job_requirements["must_have_skills"],
        job_requirements["optional_skills"]
    )

    role_text = " ".join(job_requirements["must_have_skills"])
    tfidf_raw = tfidf_similarity(role_text, resume_text)
    tfidf_score = normalize_tfidf(tfidf_raw)

    ats = (0.75 * skill_score) + (0.25 * tfidf_score)
    return round(ats, 2)


# ---------------- ML SCORE ----------------
def calculate_ml_score(resume_text, job_requirements):
    skill_score = calculate_skill_score(
        resume_text,
        job_requirements["must_have_skills"],
        job_requirements["optional_skills"]
    )

    role_text = " ".join(job_requirements["must_have_skills"])
    tfidf_raw = tfidf_similarity(role_text, resume_text)
    tfidf_score = normalize_tfidf(tfidf_raw)

    ml = (0.65 * skill_score) + (0.35 * tfidf_score)
    return round(ml, 2)


# ---------------- FINAL SCORE ----------------
def calculate_total_score(ats, ml):
    return round((ats + ml) / 2, 2)


# ---------------- MISSING SKILLS ----------------
def get_missing_skills(resume_text, must_have_skills):
    resume_text = clean_text(resume_text)
    return [skill for skill in must_have_skills if skill not in resume_text]
import re

# ---------------- ATS-CORRECT PERSONALIZED SCORING ----------------
def personalized_ats_score(text, selected_skills):
    matched = []
    missing = []

    text = text.lower()

    for skill in selected_skills:
        # ✅ Skill counted ONLY once (ATS rule)
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text):
            matched.append(skill)
        else:
            missing.append(skill)

    if not selected_skills:
        return 0, [], []

    score = (len(matched) / len(selected_skills)) * 100

    return round(score, 2), matched, missing


import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()