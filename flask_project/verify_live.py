import requests
import uuid

def main():
    s = requests.Session()
    base_url = 'http://127.0.0.1:5000'

    # 1. Home Page (home.html)
    r = s.get(f'{base_url}/')
    assert r.status_code == 200, f"Home failed: {r.status_code}"
    assert 'Home Page (home.html)' in r.text
    assert 'Library Management System' in r.text
    assert 'Sign Up' in r.text and 'Login' in r.text
    print('[PASS] 1. Home Page (home.html): OK')

    # 2. Sign Up Page (signup.html)
    test_user = f"user_{uuid.uuid4().hex[:5]}"
    r = s.post(f'{base_url}/signup', data={
        'name': 'Aisha Khan',
        'username': test_user,
        'password': 'password123'
    }, allow_redirects=True)
    assert r.status_code == 200, f"Signup failed: {r.status_code}"
    assert 'Login Page (login.html)' in r.text
    print(f'[PASS] 2. Sign Up Page (signup.html) -> redirect to Login Page: OK')

    # 3. Login Page (login.html) -> Dashboard Page (dashboard.html)
    r = s.post(f'{base_url}/login', data={
        'username': test_user,
        'password': 'password123'
    }, allow_redirects=True)
    assert r.status_code == 200, f"Login failed: {r.status_code}"
    assert 'Dashboard Page (dashboard.html)' in r.text
    assert 'Library Dashboard' in r.text
    assert '+ Submit (Issue Book)' in r.text
    assert 'View Book' in r.text
    print('[PASS] 3. Login Page (login.html) -> Dashboard Page (dashboard.html): OK')

    # 4. Book Issue Form Page (issue_book.html) -> Book Issued Successfully Page (success.html)
    r = s.post(f'{base_url}/issue_book', data={
        'book_id': '10',
        'book_name': 'Cloud Computing',
        'book_number': 'B010',
        'student_name': 'Meera Sen',
        'issue_date': '2025-09-22',
        'due_date': '2025-10-22'
    }, allow_redirects=True)
    assert r.status_code == 200, f"Book issue failed: {r.status_code}"
    assert 'Book Issued Successfully Page (success.html)' in r.text
    assert 'Book Issued Successfully!' in r.text
    assert 'Cloud Computing' in r.text
    assert 'Meera Sen' in r.text
    print('[PASS] 4. Book Issue Form (issue_book.html) -> Success Page (success.html): OK')

    # 5. Book Details / List Page (view_books.html)
    r = s.get(f'{base_url}/view_books')
    assert r.status_code == 200, f"View books failed: {r.status_code}"
    assert 'Book Details / List Page (view_books.html)' in r.text
    assert 'Python Basics' in r.text
    assert 'Data Structures' in r.text
    assert 'Web Development' in r.text
    assert 'Aisha Khan' in r.text
    print('[PASS] 5. Book Details / List Page (view_books.html): OK')

    print('\n' + '='*50)
    print('ALL 5 INFOGRAPHIC DIAGRAM FLOWS VERIFIED 100% OK!')
    print('='*50)

if __name__ == '__main__':
    main()
