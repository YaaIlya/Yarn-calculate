# tests/test_app.py
import unittest
import os
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_yarns_page(self):
        response = self.app.get('/yarns')
        self.assertEqual(response.status_code, 200)

    def test_readme_file(self):
        # Проверяем, существует ли файл readme.txt
        self.assertTrue(os.path.exists('readme.txt'))

if __name__ == "__main__":
    unittest.main()
