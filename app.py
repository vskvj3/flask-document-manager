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
    documents_list = []
    for document in document_files:
        documents_list.append({
            'id': document[0],
            'title': document[1],
            'description': document[2],
            'file_path': document[3]
        })
    return render_template('index.html', documents=documents_list)

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


@app.route('/download/<int:id>')
def download_document(id):
    document_file = documents.get_document(id)
    return send_file(document_file[3], as_attachment=True)
            

    return render_template('upload.html')
if __name__ == '__main__':
    app.run(debug=True)