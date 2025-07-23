from flask import Flask, request, jsonify, render_template
import fitz  # pymupdf
import os
import spacy

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

nlp = spacy.load("en_core_web_sm")

# Example skill list (in real case, pull from database or file)
SKILL_KEYWORDS = [
    "python", "machine learning", "deep learning", "nlp", "data analysis",
    "tensorflow", "pandas", "flask", "sql", "communication", "leadership"
]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    file = request.files['resume']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    text = extract_text_from_pdf(filepath)
    found_skills = extract_skills(text)
    return jsonify({"skills": found_skills})

def extract_text_from_pdf(path):
    text = ""
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_skills(resume_text):
    doc = nlp(resume_text.lower())
    tokens = [token.text for token in doc if not token.is_stop and token.is_alpha]
    found = set()
    for skill in SKILL_KEYWORDS:
        if skill in tokens:
            found.add(skill)
    return list(found)

if __name__ == '__main__':
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(debug=True)