from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from utils import (
    extract_text_from_pdf,
    extract_skills,
    calculate_ats_score,
    calculate_ml_score
)
from skills_db import JOB_ROLES

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        role = request.form["job_role"]
        role_data = JOB_ROLES[role]
        required_skills = role_data["skills"]
        job_description = role_data["description"]

        resumes = request.files.getlist("resume")
        results = []

        for resume in resumes:
            filename = secure_filename(resume.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            resume.save(path)

            text = extract_text_from_pdf(path)

            found_skills = extract_skills(text, required_skills)
            missing_skills = list(set(required_skills) - set(found_skills))

            ats_score = calculate_ats_score(found_skills, required_skills)
            ml_score = calculate_ml_score(text, job_description)

            # 🔥 HYBRID SCORE
            final_score = round((ats_score * 0.6) + (ml_score * 0.4), 2)

            results.append({
                "name": filename,
                "ats_score": ats_score,
                "ml_score": ml_score,
                "final_score": final_score,
                "missing_skills": missing_skills
            })

        ranked = sorted(results, key=lambda x: x["final_score"], reverse=True)

        for i, r in enumerate(ranked, start=1):
            r["rank"] = i

        return render_template("result.html", resumes=ranked, role=role)

    return render_template("index.html", roles=JOB_ROLES.keys())


if __name__ == "__main__":
    app.run(debug=True)
