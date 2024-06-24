import sqlite3
import os
import datetime


class DocumentManager:
    def __init__(self, db_name='data/files.sqlite'):
        """
        Initializes a DocumentManager object.

        Parameters:
            db_name (str): The name of the SQLite database file.

        Raises:
            sqlite3.Error: If there is an error connecting to the database.
            AttributeError: If there is an error creating the table.
        """
        try:
            self.connection = sqlite3.connect(db_name, check_same_thread=False)
            self.create_table()
        except sqlite3.Error as e:
            raise sqlite3.Error("Could not connect database") from e
        except AttributeError as e:
            raise AttributeError("Could not create table") from e

    def create_table(self):
        """
        Creates the 'documents' table if it doesn't exist in the database.

        Raises:
            sqlite3.Error: If there is an error creating the table.
        """
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
        """
        Adds a new document to the 'documents' table.

        Parameters:
            title (str): The title of the document.
            description (str): The description of the document.
            file_path (str): The file path of the document.

        Raises:
            sqlite3.Error: If there is an error adding the document to the table.
        """
        try:
            # 
            with self.connection:
                self.connection.execute(
                    '''
                    INSERT INTO documents (title, description, file_path)
                    VALUES (?, ?, ?)
                    ''', (title, description, file_path))
        except sqlite3.Error as e:
            raise sqlite3.Error("Could not add document", e) from e

    def delete_document(self, id):
        """
        Removes an entry from the 'documents' table using the specified id.

        Parameters:
            id (int): The id of the document to be deleted.

        Raises:
            sqlite3.Error: If there is an error deleting the document from the table.
        """
        try:
            with self.connection:
                self.connection.execute(
                    '''
                    DELETE FROM documents WHERE id=?
                    ''', (id,))
        except sqlite3.Error as e:
            raise sqlite3.Error("Could not delete document") from e
        
    def update_document(self, id, update_dict):
        """
         Updates a document in the 'documents' table using the specified id and update dictionary.

        Parameters:
            id (int): The id of the document to be updated.
            update_dict (dict): A dictionary containing the fields to be updated.

        Raises:
            sqlite3.Error: If there is an error updating the document in the table.
        """
        try:
            with self.connection:
                update_query = "UPDATE documents SET "
                update_values = []
                for key, value in update_dict.items():
                    update_query += f"{key}=?, "
                    update_values.append(value)
                update_query = update_query.rstrip(", ")
                update_query += " WHERE id=?"
                update_values.append(id)
                self.connection.execute(update_query, update_values)
        except sqlite3.Error as e:
            raise sqlite3.Error("Could not update document") from e

    def get_document(self, id):
        """
        Retrieves a document from the 'documents' table using the specified id.

        Parameters:
            id (int): The id of the document to be retrieved.

        Returns:
            dict: A dictionary containing the document information.

        Raises:
            sqlite3.Error: If there is an error retrieving the document from the table.
        """
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
        """
        Retrieves all documents from the 'documents' table.

        Returns:
            list: A list of dictionaries, each containing the document information.

        Raises:
            sqlite3.Error: If there is an error retrieving the documents from the table.
        """
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
