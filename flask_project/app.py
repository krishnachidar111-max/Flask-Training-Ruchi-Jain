import os
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'library-management-system-secret-key-2026')

# Database Configuration with intelligent fallback:
# If MySQL is accessible, use it; otherwise seamlessly fall back to SQLite.
mysql_uri = os.environ.get('MYSQL_URI', 'mysql+pymysql://root:@localhost/FLask%20Project')
sqlite_uri = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'library.db')

database_uri = sqlite_uri
if os.environ.get('USE_MYSQL', '0') == '1':
    try:
        import pymysql
        conn = pymysql.connect(host='localhost', user='root', password='', database='ruchijain')
        conn.close()
        database_uri = mysql_uri
        print("Connected to MySQL database successfully!")
    except Exception as e:
        print(f"MySQL unavailable ({e}), falling back to SQLite: {sqlite_uri}")
        database_uri = sqlite_uri
else:
    database_uri = os.environ.get('DATABASE_URL', sqlite_uri)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/FLask%20Project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print('Krishna')

db = SQLAlchemy(app)

# ----------------- Database Models -----------------

# 1. User Model for Authentication (Matches Sign Up & Login)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# 2. Book Issue Model (Matches Book Issue Form & Book Details/List Page)
class IssuedBook(db.Model):
    __tablename__ = 'issued_books'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.String(50), nullable=True)        # BookID in diagram
    book_name = db.Column(db.String(150), nullable=False)     # Book Name
    book_number = db.Column(db.String(50), nullable=False)    # Book Number (e.g. B001)
    student_name = db.Column(db.String(100), nullable=False)  # Name of Student
    issue_date = db.Column(db.String(20), nullable=False)     # Issue Date (YYYY-MM-DD)
    due_date = db.Column(db.String(20), nullable=False)       # Due Date (YYYY-MM-DD)
    student_id = db.Column(db.String(50), nullable=True)      # Backward compatibility
    department = db.Column(db.String(100), nullable=True)
    return_date = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default='Issued')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

# 3. Preserved Contact Model
class ContactUser(db.Model):
    __tablename__ = 'contact_users'
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_num = db.Column(db.String(20), nullable=False)
    meg = db.Column(db.String(255), nullable=True)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please login to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Initialize Database and Seed Sample Data
with app.app_context():
    db.create_all()

    # Seed demo user
    if User.query.count() == 0:
        demo_user = User(name="Library Admin", username="admin")
        demo_user.set_password("admin123")
        db.session.add(demo_user)
        db.session.commit()
        print("Demo account created: username 'admin', password 'admin123'")

    # Seed sample books matching exact diagram data
    if IssuedBook.query.count() == 0:
        sample_books = [
            IssuedBook(
                book_id="1",
                book_name="Python Basics",
                book_number="B001",
                student_name="Krishna Chidar",
                issue_date="2025-09-10",
                due_date="2025-10-10",
                status="Issued"
            ),
            IssuedBook(
                book_id="2",
                book_name="Data Structures",
                book_number="B002",
                student_name="Rohit Sharma",
                issue_date="2025-09-12",
                due_date="2025-10-12",
                status="Issued"
            ),
            IssuedBook(
                book_id="3",
                book_name="Web Development",
                book_number="B003",
                student_name="Neha Singh",
                issue_date="2025-09-15",
                due_date="2025-10-15",
                status="Issued"
            ),
        ]
        db.session.bulk_save_objects(sample_books)
        db.session.commit()
        print("Sample books seeded successfully!")

# ----------------- Routes Matching Diagram Exactly -----------------

# 1. Home Page (home.html)
@app.route("/")
def home():
    return render_template("home.html")

# 2. Sign Up Page (signup.html)
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not name or not username or not password:
            flash("All fields are required.", "danger")
            return render_template("signup.html")

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already taken. Please choose another.", "danger")
            return render_template("signup.html")

        # Save user data to Database
        new_user = User(name=name, username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template("signup.html")

# 3. Login Page (login.html)
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['name'] = user.name
            flash(f"Welcome, {user.name}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "danger")
            return render_template("login.html")

    return render_template("login.html")

# Logout Route
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

# 4. Dashboard Page (dashboard.html)
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# 5. Book Issue Form Page (issue_book.html)
@app.route("/issue_book", methods=['GET', 'POST'])
@app.route("/book_issue", methods=['GET', 'POST'])
@login_required
def issue_book():
    if request.method == 'POST':
        book_id = request.form.get('book_id', '').strip()
        book_name = request.form.get('book_name', '').strip()
        book_number = request.form.get('book_number', '').strip()
        student_name = request.form.get('student_name', '').strip()
        issue_date = request.form.get('issue_date', '').strip()
        due_date = request.form.get('due_date', '').strip()

        if not all([book_id, book_name, book_number, student_name, issue_date, due_date]):
            flash("Please fill in all form fields.", "danger")
            return render_template("issue_book.html")

        # Save book issue data to Database
        issue_entry = IssuedBook(
            book_id=book_id,
            book_name=book_name,
            book_number=book_number,
            student_name=student_name,
            issue_date=issue_date,
            due_date=due_date,
            student_id=book_id,
            department='',
            return_date=due_date,
            status='Issued'
        )
        db.session.add(issue_entry)
        db.session.commit()

        # After successful submission, redirect to Book Issued Successfully Page
        return redirect(url_for('success', book_id=issue_entry.id))

    return render_template("issue_book.html")

# 6. Book Issued Successfully Page (success.html)
@app.route("/success/<int:book_id>")
@app.route("/issue_success/<int:book_id>")
@login_required
def success(book_id):
    book = db.get_or_404(IssuedBook, book_id)
    return render_template("success.html", book=book)

# 7. Book Details / List Page (view_books.html)
@app.route("/view_books")
@app.route("/book_details")
@login_required
def view_books():
    books = IssuedBook.query.order_by(IssuedBook.id.asc()).all()
    return render_template("view_books.html", books=books)

# Preserved Contact Routes
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            message = request.form.get('message')
            
            entry = ContactUser(name=name, email=email, phone_num=phone, meg=message)
            db.session.add(entry)
            db.session.commit()
            flash("Contact message sent successfully!", "success")
        except Exception as e:
            flash(f"Failed to submit message: {e}", "danger")
    return render_template('contact.html')

@app.route("/contacts")
def contacts():
    all_contacts = ContactUser.query.all()
    return render_template('contacts.html', contacts=all_contacts)

if __name__ == "__main__":
    app.run(debug=True, port=5000)