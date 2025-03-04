from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
import pdfkit
from ml_helper import generate_resume_suggestions

app = Flask(__name__)
CORS(app)

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['resume_builder']
resumes = db['resumes']

@app.route('/api/resume/create', methods=['POST'])
def create_resume():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    education = data.get('education')
    experience = data.get('experience')
    skills = data.get('skills')
    job_role = data.get('jobRole')

    # Save resume to MongoDB
    resume = {
        'name': name,
        'email': email,
        'education': education,
        'experience': experience,
        'skills': skills,
        'jobRole': job_role,
    }
    result = resumes.insert_one(resume)
    resume_id = str(result.inserted_id)

    # Generate AI suggestions
    suggestions = generate_resume_suggestions(resume)

    return jsonify({
        'status': 'success',
        'data': {
            'resume_id': resume_id,
            'suggestions': suggestions,
        },
    })

@app.route('/api/resume/download/<resume_id>', methods=['GET'])
def download_resume(resume_id):
    resume = resumes.find_one({'_id': resume_id})
    if not resume:
        return jsonify({'status': 'fail', 'message': 'Resume not found'}), 404

    # Generate PDF
    html_content = f"""
    <h1>{resume['name']}</h1>
    <p>{resume['email']}</p>
    <h2>Education</h2>
    <p>{'<br>'.join(resume['education'])}</p>
    <h2>Experience</h2>
    <p>{'<br>'.join(resume['experience'])}</p>
    <h2>Skills</h2>
    <p>{'<br>'.join(resume['skills'])}</p>
    """
    pdfkit.from_string(html_content, 'resume.pdf')

    return send_file('resume.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)