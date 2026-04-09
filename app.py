import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from utils.parser import extract_text
from utils.analyzer import extract_keywords, match_skills, generate_feedback
from utils.scorer import calculate_similarity

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("resume")
    job_desc = request.form.get("job_desc", "").strip()

    if not file or not job_desc:
        return "❌ Please upload resume and enter job description"

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    resume_text = extract_text(filepath)

    if not resume_text.strip():
        return "❌ Unable to extract text from resume"

    # Keywords
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_desc)

    # Skills
    resume_skills = match_skills(resume_text)
    job_skills = match_skills(job_desc)

    missing_skills = sorted(list(set(job_skills) - set(resume_skills)))

    # Score
    score = calculate_similarity(resume_text, job_desc)

    # Feedback
    feedback = generate_feedback(resume_text, job_desc, missing_skills, score)

    return render_template(
        "result.html",
        score=score,
        missing_skills=missing_skills,
        feedback=feedback,
        resume_skills=resume_skills,
        job_skills=job_skills
    )


if __name__ == "__main__":
    app.run(debug=True)