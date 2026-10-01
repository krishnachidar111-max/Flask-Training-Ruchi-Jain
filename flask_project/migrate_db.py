import sqlite3

def migrate():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    cursor.execute('PRAGMA table_info(issued_books)')
    cols = [c[1] for c in cursor.fetchall()]

    if 'book_id' not in cols:
        cursor.execute('ALTER TABLE issued_books ADD COLUMN book_id VARCHAR(50)')
    if 'due_date' not in cols:
        cursor.execute('ALTER TABLE issued_books ADD COLUMN due_date VARCHAR(20)')

    # Clear and populate exact infographic data
    cursor.execute('DELETE FROM issued_books')
    records = [
        (1, '1', 'Krishna Chidar', 'Python Basics', 'B001', '2025-09-10', '2025-10-10', 'Issued'),
        (2, '2', 'Rohit Sharma', 'Data Structures', 'B002', '2025-09-12', '2025-10-12', 'Issued'),
        (3, '3', 'Neha Singh', 'Web Development', 'B003', '2025-09-15', '2025-10-15', 'Issued')
    ]

    cursor.executemany('''
    INSERT INTO issued_books (id, book_id, student_name, book_name, book_number, issue_date, due_date, status, student_id, department, return_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, '', ?)
    ''', [(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[1], r[6]) for r in records])

    conn.commit()
    cursor.execute('SELECT id, book_id, book_name, book_number, student_name, issue_date, due_date FROM issued_books')
    for row in cursor.fetchall():
        print("Migrated Row:", row)
    conn.close()

if __name__ == '__main__':
    migrate()
