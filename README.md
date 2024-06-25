# Flask Document Manager
### Project Structure
```
DocumentManger-Visakh/
    data/
        files.sqlite
    templates/
        base.html
        index.html
        update.html
        upload.html
        view.html
    uploads/
    app.py
    documet_manager.py
```
#### /data
- this folder contains the database.
#### templates/
- jinja2 templated form the UI.
#### uploads/
- folder to store uploaded files.
#### app.py
- flask application.
#### document_manager.py
- module with DocumentManager class to handle the database operations.
  

### How to run the app
Install dependencies:
```bash
pip install -r requirements.txt
```
Run the flask app:
```bash
python app.py
```
### Packages Used
- datetime: store upload time. 
- sqlite3: database operations.
- os: file handling.
- flask_wtf: wtforms support in flask.
- pylint: linting python files.
- djlint: linting jinja2 templates.

### Design
- UI of the flask app is developed using bootstrap with jinja templates.
- Initial home page of the application will have a list of uploaded files.
- Option to upload more files will be available on the sidebar.
- Options for more operations(Update, Delete etc.) will be available by clicking the view button.
- Upload and updation forms are built using flask_wtf with CSRF protection.
- Status of operations are passed as ```Flask Flashing``` technique and is rendered on the sidebar using bootstrap alerts.
  