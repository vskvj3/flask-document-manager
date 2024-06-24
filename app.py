from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
from document import DocumentManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'

documents = DocumentManager()

@app.route('/')
def index():
    document_files = documents.get_all_documents()
    print(document_files)
    
    return render_template('index.html', documents=document_files)

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
            print('Document uploaded successfully!')
            return redirect(url_for('index'))
        else:
            print('No file selected!')

@app.route('/document/<int:id>')
def view_document(id):
    document_file = documents.get_document(id)
    return render_template('view.html', document=document_file)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_document(id):
    document = documents.get_document(id)
    print(document)
    if request.method == 'POST':
        document.title = request.form['title']
        document.description = request.form['description']
        file = request.files['file']
        
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            document.file_path = file_path
        
        return redirect(url_for('index'))
    
    return render_template('update.html', document=document)

@app.route('/download/<int:id>')
def download_document(id):
    document_file = documents.get_document(id)
    return send_file(document_file[3], as_attachment=True)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_document(id):
    document_file = documents.get_document(id)
    os.remove(document_file[3])
    documents.delete_document(id)
    return redirect(url_for('index'))




            

    return render_template('upload.html')
if __name__ == '__main__':
    app.run(debug=True)