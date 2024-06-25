"""
Module for testing the DocumentManager class.
"""
import unittest
from document_manager import DocumentManager


class DocumentManagerTests(unittest.TestCase):
    """
    Test the DocumentManager class.
    """

    def setUp(self):
        """
        Create a DocumentManager instance and create the table.
        """
        self.manager = DocumentManager(':memory:')
        self.manager.create_table()

    def tearDown(self):
        """
        Close the connection to the database.
        """
        self.manager.connection.close()

    def test_add_document(self):
        """
        Test the add_document method.
        """
        self.manager.add_document(
            'Document 1', 'Description 1', '2022-01-01', '/path/to/document1')
        self.manager.add_document(
            'Document 2', 'Description 2', '2022-01-02', '/path/to/document2')
        documents = self.manager.get_all_documents()
        self.assertEqual(len(documents), 2)
        self.assertEqual(documents[0]['title'], 'Document 1')
        self.assertEqual(documents[1]['description'], 'Description 2')

    def test_delete_document(self):
        """
        Test the delete_document method.
        """
        self.manager.add_document(
            'Document 1', 'Description 1', '2022-01-01', '/path/to/document1')
        self.manager.add_document(
            'Document 2', 'Description 2', '2022-01-02', '/path/to/document2')
        documents = self.manager.get_all_documents()
        self.assertEqual(len(documents), 2)
        self.manager.delete_document(documents[0]['doc_id'])
        documents = self.manager.get_all_documents()
        self.assertEqual(len(documents), 1)
        self.assertEqual(documents[0]['title'], 'Document 2')

    def test_update_document(self):
        """
        Test the update_document method.
        """
        self.manager.add_document(
            'Document 1', 'Description 1', '2022-01-01', '/path/to/document1')
        documents = self.manager.get_all_documents()
        self.assertEqual(len(documents), 1)
        doc_id = documents[0]['doc_id']
        self.manager.update_document(
            doc_id, {'title': 'Updated Document 1', 'description': 'Updated Description 1'})
        updated_document = self.manager.get_document(doc_id)
        self.assertEqual(updated_document['title'], 'Updated Document 1')
        self.assertEqual(
            updated_document['description'], 'Updated Description 1')

    def test_get_document(self):
        """
        Test the get_document method.
        """
        self.manager.add_document(
            'Document 1', 'Description 1', '2022-01-01', '/path/to/document1')
        documents = self.manager.get_all_documents()
        self.assertEqual(len(documents), 1)
        doc_id = documents[0]['doc_id']
        document = self.manager.get_document(doc_id)
        self.assertEqual(document['title'], 'Document 1')
        self.assertEqual(document['description'], 'Description 1')

    def test_get_all_documents(self):
        """
        Test the get_all_documents method.
        """
        self.manager.add_document(
            'Document 1', 'Description 1', '2022-01-01', '/path/to/document1')
        self.manager.add_document(
            'Document 2', 'Description 2', '2022-01-02', '/path/to/document2')
        documents = self.manager.get_all_documents()
        self.assertEqual(len(documents), 2)
        self.assertEqual(documents[0]['title'], 'Document 1')
        self.assertEqual(documents[1]['title'], 'Document 2')


if __name__ == '__main__':
    unittest.main()
