import sqlite3


class DocumentManager:
    def __init__(self, db_name='data/files.sqlite'):
        try:
            self.connection = sqlite3.connect(db_name, check_same_thread=False)
            self.create_table()
        except sqlite3.Error as e:
            raise sqlite3.Error("Could not connect database") from e
        except AttributeError as e:
            raise AttributeError("Could not create table") from e

    def create_table(self):
        try:
            with self.connection:
                self.connection.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS documents (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        description TEXT,
                        file_path TEXT
                    )''')
        except sqlite3.Error as e:
            raise sqlite3.Error("Could not create database") from e

    def add_document(self, title, description, file_path):
        try:
            with self.connection:
                self.connection.execute(
                    '''
                    INSERT INTO documents (title, description, file_path)
                    VALUES (?, ?, ?)
                    ''', (title, description, file_path))
        except sqlite3.Error as e:
            raise sqlite3.Error("Could not add document", e) from e

    def get_document(self, id):
        try:
            with self.connection:
                cursor = self.connection.execute(
                    '''
                    SELECT * FROM documents WHERE id=?
                    ''', (id,))
                document = cursor.fetchone()
                document_dict = {
                    'id': document[0],
                    'title': document[1],
                    'description': document[2],
                    'file_path': document[3]
                }
                return document_dict
        except sqlite3.Error as e:
            raise sqlite3.Error("Could not get document") from e

    def get_all_documents(self):
        try:
            with self.connection:
                cursor = self.connection.execute(
                    '''
                    SELECT * FROM documents
                    ''')
                document_files = cursor.fetchall()
            documents_list = []
            for document in document_files:
                documents_list.append({
                    'id': document[0],
                    'title': document[1],
                    'description': document[2],
                    'file_path': document[3]
                })
            return documents_list

        except sqlite3.Error as e:
            raise sqlite3.Error("Could not get document") from e
