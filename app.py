from flask import Flask, render_template, request, redirect, url_for, flash
import os
from document import DocumentManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'

documents = DocumentManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files['file']
        
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            documents.add_document(title, description, file_path)
            flash('Document uploaded successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('No file selected!', 'danger')
    
    return render_template('upload.html')
if __name__ == '__main__':
    app.run(debug=True)