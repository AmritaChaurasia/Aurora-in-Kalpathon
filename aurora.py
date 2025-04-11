from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy skill extractor (simulates analyzing resume filename)
def extract_skills_from_resume(filename):
    if 'data' in filename:
        return ["Python", "pandas", "Statistics"]
    elif 'full' in filename:
        return ["HTML", "CSS", "JavaScript"]
    elif 'graphic' in filename:
        return ["Photoshop", "Creativity"]
    return []

def generate_suggestions(job, extracted_skills):
    job = job.lower()
    required_skills, learning_resources = [], []

    if "data scientist" in job:
        required_skills = ["Python", "pandas", "NumPy", "scikit-learn", "Statistics", "Machine Learning", "Data Visualization"]
        learning_resources = ["Data Science Specialization - Coursera", "Kaggle Learn Courses", "Python for Data Science - freeCodeCamp"]
    elif "full stack" in job:
        required_skills = ["HTML", "CSS", "JavaScript", "React", "Node.js", "Express", "MongoDB", "PostgreSQL"]
        learning_resources = ["Full-Stack Web Development Bootcamp - Udemy", "The Odin Project", "freeCodeCamp Full Stack Path"]
    elif "graphic designer" in job:
        required_skills = ["Typography", "Color Theory", "UI/UX Design", "Figma", "Adobe Photoshop", "Adobe Illustrator", "Creativity", "Layout Design"]
        learning_resources = ["Graphic Design Specialization - Coursera", "Learn Figma for UI/UX Design - Udemy", "Canva Design School"]
    else:
        required_skills = ["Time Management", "Communication Skills", "Problem Solving", "Team Collaboration"]
        learning_resources = ["Soft Skills for Professionals - Coursera", "Communication Skills Mastery - Udemy", "Teamwork Skills - LinkedIn Learning"]

    matched_skills = [skill for skill in extracted_skills if skill in required_skills]

    return required_skills, matched_skills, learning_resources

HTML_FORM = '''
<!doctype html>
<title>Resume AI Chatbot</title>
<h2>Resume Skill Advisor</h2>
<form method=post enctype=multipart/form-data>
  Name: <input type=text name=name><br><br>
  Upload Resume (PDF): <input type=file name=resume><br><br>
  Dream Job: <input type=text name=dream_job><br><br>
  <input type=submit value='Analyze'>
</form>
{% if result %}
  <h3>Skill Analysis:</h3>
  <table border="1" cellpadding="10">
    <tr><th>Required Skills</th><th>Skills in Resume</th><th>Learning Resources</th></tr>
    <tr>
      <td>{{ result.required }}</td>
      <td>{{ result.present }}</td>
      <td>{{ result.resources }}</td>
    </tr>
  </table>
{% endif %}
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    result = None
    if request.method == 'POST':
        name = request.form['name']
        dream_job = request.form['dream_job']
        file = request.files['resume']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        extracted_skills = extract_skills_from_resume(filename)
        required, present, resources = generate_suggestions(dream_job, extracted_skills)

        result = {
            'required': ", ".join(required),
            'present': ", ".join(present) or "None",
            'resources': ", ".join(resources)
        }

    return render_template_string(HTML_FORM, result=result)

if __name__ == '__main__':
    app.run(debug=True)
