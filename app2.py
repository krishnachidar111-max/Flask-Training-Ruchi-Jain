from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Application & Database Configuration
app.config['SECRET_KEY'] = 'thisisasecretkey'
# Driver name for mysqlclient is 'mysql+mysqldb'. Use %20 for spaces in DB name.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:@localhost/FLask%20Project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database instance with the Flask app
db = SQLAlchemy(app)
print("krishna")

# Database Model
class User(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(50), nullable=False)

# Create tables inside app context
with app.app_context():
    db.create_all()

# Always run the development server at the end of the file
if __name__ == '__main__':
    app.run(debug=True)