import unittest
import uuid
from app import app, db, User, IssuedBook

class LibrarySystemDiagramTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home Page (home.html)', response.data)
        self.assertIn(b'Library Management System', response.data)
        self.assertIn(b'Sign Up', response.data)
        self.assertIn(b'Login', response.data)

    def test_signup_and_login_flow(self):
        test_user = f"user_{uuid.uuid4().hex[:6]}"
        # Sign up
        response = self.client.post('/signup', data={
            'name': 'Aisha Khan',
            'username': test_user,
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful', response.data)
        self.assertIn(b'Login Page (login.html)', response.data)

        # Login
        response = self.client.post('/login', data={
            'username': test_user,
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard Page (dashboard.html)', response.data)
        self.assertIn(b'Library Dashboard', response.data)
        self.assertIn(b'+ Submit (Issue Book)', response.data)
        self.assertIn(b'View Book', response.data)

    def test_issue_book_and_success_flow(self):
        # Login
        self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)

        # Issue book
        response = self.client.post('/issue_book', data={
            'book_id': '4',
            'book_name': 'Operating Systems',
            'book_number': 'B004',
            'student_name': 'Karan Singh',
            'issue_date': '2025-09-20',
            'due_date': '2025-10-20'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book Issued Successfully Page (success.html)', response.data)
        self.assertIn(b'Book Issued Successfully!', response.data)
        self.assertIn(b'Operating Systems', response.data)
        self.assertIn(b'Karan Singh', response.data)

    def test_view_books_page(self):
        self.client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        response = self.client.get('/view_books')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book Details / List Page (view_books.html)', response.data)
        self.assertIn(b'Python Basics', response.data)
        self.assertIn(b'Aisha Khan', response.data)
        self.assertIn(b'B001', response.data)

if __name__ == '__main__':
    unittest.main()
