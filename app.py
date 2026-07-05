from flask import Flask, render_template, request
import pdfplumber
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Skills Database
skills_list = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "nodejs",
    "flask",
    "django",
    "mysql",
    "mongodb",
    "machine learning",
    "deep learning",
    "data analysis",
    "power bi",
    "git",
    "github",
    "aws",
    "azure",
    "docker",
    "kubernetes",
    "spring boot",
    "rest api",
    "oop",
    "dbms",
    "dsa",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "excel"
]


def extract_text(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

    return text.lower()


@app.route("/", methods=["GET", "POST"])
def index():

    ats_score = 0
    found_skills = []
    missing_skills = []
    suggestions = []

    total_found = 0
    matched = 0

    if request.method == "POST":

        resume = request.files["resume"]

        if not resume.filename.endswith(".pdf"):
            return "Please upload only PDF resumes."

        job_description = request.form["job_description"].lower()

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            resume.filename
        )

        resume.save(filepath)

        resume_text = extract_text(filepath)

        # Delete uploaded file
        os.remove(filepath)

        # Skills in Resume
        for skill in skills_list:
            if skill in resume_text:
                found_skills.append(skill)

        total_found = len(found_skills)

        # Skills in Job Description
        jd_skills = []

        for skill in skills_list:
            if skill in job_description:
                jd_skills.append(skill)

        # Compare Skills
        for skill in jd_skills:
            if skill in found_skills:
                matched += 1
            else:
                missing_skills.append(skill)

        # Better ATS Score
        score = 0

        if len(jd_skills) > 0:
            score += (matched / len(jd_skills)) * 60

        if "projects" in resume_text:
            score += 20

        if "internship" in resume_text:
            score += 10

        if "github" in resume_text:
            score += 10

        ats_score = int(score)

        # Suggestions
        if ats_score < 50:
            suggestions.append(
                "Improve technical skills according to the Job Description."
            )

        if "projects" not in resume_text:
            suggestions.append(
                "Add a Projects section with measurable achievements."
            )

        if "github" not in resume_text:
            suggestions.append(
                "Add your GitHub profile link."
            )

        if "internship" not in resume_text:
            suggestions.append(
                "Mention internships or practical experience."
            )

        if total_found < 8:
            suggestions.append(
                "Include more technical skills."
            )

        if len(missing_skills) > 0:
            suggestions.append(
                "Add the missing skills if you possess them."
            )

    return render_template(
        "index.html",
        ats_score=ats_score,
        found_skills=found_skills,
        missing_skills=missing_skills,
        suggestions=suggestions,
        total_found=total_found,
        matched=matched
    )


if __name__ == "__main__":
    app.run(debug=True)