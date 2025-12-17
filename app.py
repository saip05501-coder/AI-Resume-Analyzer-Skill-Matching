from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from utils import extract_text_from_pdf, extract_skills, calculate_skill_score
from skills_db import JOB_ROLES

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        selected_role = request.form['job_role']
        required_skills = JOB_ROLES[selected_role]

        resumes = request.files.getlist('resume')
        results = []

        for resume in resumes:
            filename = secure_filename(resume.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume.save(path)

            resume_text = extract_text_from_pdf(path)
            found_skills = extract_skills(resume_text, required_skills)
            missing_skills = list(set(required_skills) - set(found_skills))

            score = calculate_skill_score(found_skills, required_skills)

            results.append({
                "name": filename,
                "score": score,
                "found_skills": found_skills,
                "missing_skills": missing_skills
            })

        # Rank resumes
        ranked_resumes = sorted(results, key=lambda x: x['score'], reverse=True)

        for i, r in enumerate(ranked_resumes, start=1):
            r['rank'] = i

        return render_template(
            'result.html',
            resumes=ranked_resumes,
            job_role=selected_role
        )

    return render_template('index.html', roles=JOB_ROLES.keys())


if __name__ == '__main__':
    app.run(debug=True)
