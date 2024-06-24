from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
from document import DocumentManager
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'

document_manager = DocumentManager()


@app.route('/')
def index():
    document_files = document_manager.get_all_documents()
    print(document_files)

    return render_template('index.html', documents=document_files)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files['file']

        if file:
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], file.filename)
            
            # add time with file name to avoid copy
            file_name, file_extension = os.path.splitext(file_path)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            new_file_path = f"{file_name}_{timestamp}{file_extension}"
            file_path = new_file_path
            
            file.save(file_path)
                
            document_manager.add_document(title, description, file_path)
            print('Document uploaded successfully!')
            return redirect(url_for('index'))
        else:
            print('No file selected!')
    return render_template('upload.html')


@app.route('/document/<int:id>')
def view_document(id):
    document_file = document_manager.get_document(id)
    return render_template('view.html', document=document_file)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_document(id):
    document = document_manager.get_document(id)
    print(document)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files['file']

        if file:
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            new_file_path = file_path
        
        update_dict = {}
        if title:
            update_dict['title'] = title
        if description:
            update_dict['description'] = description
        if file:
            update_dict['file_path'] = new_file_path

        document_manager.update_document(id, update_dict)
        
        print('Document updated successfully!')

        return redirect(url_for('index'))

    return render_template('update.html', document=document)


@app.route('/download/<int:id>')
def download_document(id):
    document_file = document_manager.get_document(id)
    return send_file(document_file["file_path"], as_attachment=True)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_document(id):
    try:
        document_file = document_manager.get_document(id)
        os.remove(document_file['file_path'])
        document_manager.delete_document(id)
    except FileNotFoundError as fnf:
        print("Error: ", fnf)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
