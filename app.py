from flask import Flask, request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename
from backend import get_scores
import json

app = Flask("Job Hat")

@app.route('/')
def home():
    # with open("index.html") as f:
    #     html = f.read()
    # return html
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['resume']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        # Process your file here (e.g., save it somewhere or analyze it)
        filename = secure_filename(file.filename)
        filename = os.path.join('resumes', filename)
        file.save(filename)
        
        url = "https://github.com/SimplifyJobs/New-Grad-Positions?tab=readme-ov-file"
        # Process the uploaded file to get job matches
        job_matches = get_scores(url, filename)
        
        # Delete resume as we believe in Data Privacy
        os.remove(filename)

        # Redirect to the job matches page, passing job_matches as a query parameter or session variable
        return redirect(url_for('job_matches', job_matches=job_matches))

@app.route('/job-matches')
def job_matches():
    # If passing job matches directly, adjust to receive them as a parameter or from session
    jobs = request.args.get('job_matches').replace("'", '"').replace('&amp;', '&')
    print(jobs)
    job_matches_dict = json.loads(jobs) if jobs else {}
    return render_template('job_matches.html', jobs=job_matches_dict)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)