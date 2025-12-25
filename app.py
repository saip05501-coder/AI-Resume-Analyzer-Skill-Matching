import os
import pandas as pd
from flask import Flask, render_template, request, send_file
from skills_db import ALL_SKILLS
from utils import clean_text


from utils import (
    extract_text_from_pdf,
    calculate_ats_score,
    calculate_ml_score,
    calculate_total_score,
    get_missing_skills
)

from skills_db import JOB_ROLES

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- MAIN LANDING PAGE ----------------
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

        # ---------- SORT & RANK ----------
        results.sort(key=lambda x: x["final_score"], reverse=True)

        for i, r in enumerate(results):
            r["rank"] = i + 1

        # ---------- SAVE TO EXCEL ----------
        excel_data = []
        for r in results:
            excel_data.append({
                "Rank": r["rank"],
                "Resume Name": r["name"],
                "ATS Score": r["ats_score"],
                "ML Score": r["ml_score"],
                "Final Score": r["final_score"],
                "Missing Skills": ", ".join(r["missing_skills"]) if r["missing_skills"] else "None"
            })

        df = pd.DataFrame(excel_data)
        df.to_excel("results.xlsx", index=False)

        return render_template(
            "result.html",
            resumes=results,
            role=role
        )

    return render_template(
        "index.html",
        roles=JOB_ROLES.keys()
    )


# ---------------- DOWNLOAD EXCEL ----------------
@app.route("/download_excel")
def download_excel():
    if not os.path.exists("results.xlsx"):
        return "No results available", 404

    return send_file(
        "results.xlsx",
        as_attachment=True,
        download_name="Resume_Ranking.xlsx"
    )

@app.route("/personalized", methods=["GET", "POST"])
def personalized():
    if request.method == "POST":
        selected_skills = request.form.getlist("skills")
        files = request.files.getlist("resume")

        results = []

        for file in files:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            resume_text = extract_text_from_pdf(path)

            # ATS rule: skill counted ONCE
            resume_words = set(clean_text(resume_text).split())

            matched = [s for s in selected_skills if s.lower() in resume_words]
            score = (len(matched) / len(selected_skills)) * 100 if selected_skills else 0

            results.append({
                "name": file.filename,
                "final_score": round(score, 2),
                "matched_skills": matched,
                "missing_skills": list(set(selected_skills) - set(matched))
            })

        results.sort(key=lambda x: x["final_score"], reverse=True)

        for i, r in enumerate(results):
            r["rank"] = i + 1

        return render_template("personalized_result.html", results=results)

    return render_template("personalized.html", skills=ALL_SKILLS)



if __name__ == "__main__":
    app.run(debug=True)