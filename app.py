from flask import Flask, render_template, request
import pdfplumber
import os

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Skills database
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
    "data analysis",
    "power bi",
    "git",
    "github",
    "aws",
    "spring boot",
    "rest api",
    "oop",
    "dbms",
    "dsa"
]


# Extract text from PDF
def extract_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text.lower()


@app.route('/', methods=['GET', 'POST'])
def index():

    ats_score = 0
    found_skills = []
    missing_skills = []
    suggestions = []

    if request.method == 'POST':

        # Get uploaded file
        resume = request.files['resume']

        # Get job description
        job_description = request.form[
            'job_description'
        ].lower()

        # Save uploaded resume
        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            resume.filename
        )

        resume.save(filepath)

        # Extract resume text
        resume_text = extract_text(filepath)

        # Find skills in resume
        for skill in skills_list:

            if skill in resume_text:
                found_skills.append(skill)

        # Find skills in JD
        jd_skills = []

        for skill in skills_list:

            if skill in job_description:
                jd_skills.append(skill)

        # Compare skills
        matched = 0

        for skill in jd_skills:

            if skill in found_skills:
                matched += 1

            else:
                missing_skills.append(skill)

        # Calculate ATS score
        if len(jd_skills) > 0:

            ats_score = int(
                (matched / len(jd_skills)) * 100
            )

        # Suggestions
        if ats_score < 50:

            suggestions.append(
                "Add more relevant technical skills."
            )

        if "projects" not in resume_text:

            suggestions.append(
                "Add a strong projects section."
            )

        if "github" not in resume_text:

            suggestions.append(
                "Add GitHub profile link."
            )

        if "internship" not in resume_text:

            suggestions.append(
                "Add internship or practical experience."
            )

        if len(found_skills) < 5:

            suggestions.append(
                "Include more technical skills in resume."
            )

    return render_template(
        'index.html',
        ats_score=ats_score,
        found_skills=found_skills,
        missing_skills=missing_skills,
        suggestions=suggestions
    )


if __name__ == '__main__':

    app.run(debug=True)