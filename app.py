'''
Flask Application
'''

import os
import datetime
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from document import DocumentManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'

document_manager = DocumentManager()


@app.route('/')
def index():
    """
    Renders the index page with a list of all documents.

    Returns:
        The rendered index.html template with the documents.
    """
    try:
        document_files = document_manager.get_all_documents()
        return render_template('index.html', documents=document_files)
    except sqlite3.Error:
        flash('Could not get documents', 'error')
        return render_template('index.html', documents=[])


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """
    Handles the upload of a new document.

    Returns:
        If the request method is GET, renders the upload.html template.
        If the request method is POST, stores the file and stored the data in db.
        If the request method is POST and no file is selected, prints an error message.
    """
    if request.method == 'POST':
        try:
            title = request.form['title']
            description = request.form['description']
            file = request.files['file']

            if file:
                file_path = os.path.join(
                    app.config['UPLOAD_FOLDER'], file.filename)

                # add time with file name to avodoc_id copy
                file_name, file_extension = os.path.splitext(file_path)
                timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                new_file_path = f'{file_name}_{timestamp}{file_extension}'
                file_path = new_file_path

                file.save(file_path)

                document_manager.add_document(title, description, file_path)
                flash('Document uploaded successfully!')
            return redirect(url_for('index'))
        except sqlite3.Error:
            flash("Could not upload document")
            return render_template('upload.html')
        except PermissionError as e:
            flash("Error: " + str(e))
            return render_template('upload.html')
    return render_template('upload.html')


@app.route('/document/<int:doc_id>')
def view_document(doc_id):
    """
    Renders the view page for a specific document.

    Args:
        doc_id (int): The doc_id of the document to view.

    Returns:
        The rendered view.html template with the document.
    """
    try:
        document_file = document_manager.get_document(doc_id)
    except sqlite3.Error:
        flash('Could not get document', 'error')
        document_file = {}
    return render_template('view.html', document=document_file)


@app.route('/update/<int:doc_id>', methods=['GET', 'POST'])
def update_document(doc_id):
    """
    Handles the update of a document.

    Args:
        doc_id (int): The doc_id of the document to update.

    Returns:
        If the request method is GET, renders the update.html template.
        If the request method is POST, updates the document with given data.
    """

    if request.method == 'POST':
        try:
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

            document_manager.update_document(doc_id, update_dict)

            flash('Document updated successfully!', 'success')
        except sqlite3.Error:
            flash('Could not update document' , 'error')
        return redirect(url_for('index'))

    try:
        document = document_manager.get_document(doc_id)
    except sqlite3.Error:
        flash('Could not get document', 'error')
        document = {}
    return render_template('update.html', document=document)


@app.route('/download/<int:doc_id>')
def download_document(doc_id):
    """
    Downloads a specific document.

    Args:
        doc_id (int): The doc_id of the document to download.

    Returns:
        The document file as an attachment.
    """
    try:
        document_file = document_manager.get_document(doc_id)
        flash('Document downloaded successfully!', 'success')
        return send_file(document_file["file_path"], as_attachment=True)
    except FileNotFoundError:
        flash('File not found!!', 'error')
        return redirect(url_for('index'))
    except sqlite3.Error:
        flash('Could not find document in database', 'error')
        return redirect(url_for('index'))


@app.route('/delete/<int:doc_id>', methods=['POST'])
def delete_document(doc_id):
    """
    Deletes a specific document.

    Args:
        doc_id (int): The doc_id of the document to delete.

    Returns:
        Redirects to the index page after deleting the document.
    """
    try:
        document_file = document_manager.get_document(doc_id)
        os.remove(document_file['file_path'])
        document_manager.delete_document(doc_id)
        flash('Document deleted successfully', 'success')
    except FileNotFoundError:
        flash('File not found!!', 'error')
    except sqlite3.Error:
        flash('Could not delete document', 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
