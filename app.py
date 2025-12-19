import os
from flask import Flask, render_template, request
from utils import *
from skills_db import JOB_ROLES

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- MAIN PAGE (2 OPTIONS) ----------------
@app.route("/")
def main():
    return render_template("main.html")


# ---------------- INTRO PAGE (DO NOT DELETE) ----------------
@app.route("/rank")
def rank_intro():
    return render_template("home.html")


# ---------------- ACTUAL RESUME ANALYZER ----------------
@app.route("/analyze", methods=["GET", "POST"])
def analyze():
    if request.method == "POST":
        role = request.form["job_role"]
        files = request.files.getlist("resume")

        job_requirements = JOB_ROLES[role]
        results = []

        for file in files:
            if file.filename == "":
                continue

            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            resume_text = extract_text_from_pdf(path)

            ats = calculate_ats_score(resume_text, job_requirements)
            ml = calculate_ml_score(resume_text, job_requirements)
            final = calculate_total_score(ats, ml)

            missing = get_missing_skills(
                resume_text,
                job_requirements["must_have_skills"]
            )

            results.append({
                "name": file.filename,
                "ats_score": ats,
                "ml_score": ml,
                "final_score": final,
                "missing_skills": missing
            })

        results.sort(key=lambda x: x["final_score"], reverse=True)

        for i, r in enumerate(results):
            r["rank"] = i + 1

        return render_template("result.html", resumes=results, role=role)

    return render_template("index.html", roles=JOB_ROLES.keys())


if __name__ == "__main__":
    app.run(debug=True)
