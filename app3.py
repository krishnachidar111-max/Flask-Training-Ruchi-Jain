from flask import Flask ,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
#database configuration code
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/FLask%20Project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print('krishna')
db = SQLAlchemy(app)

# database model
class emp(db.Model):
    eid = db.Column(db.Integer, primary_key=True)
    ename = db.Column(db.String(100), nullable=True)
    ecmp = db.Column(db.String(255), nullable=True)
    sephoneno = db.Column(db.String(30), nullable=True)
    emsg = db.Column(db.String(1000), nullable=True)

with app.app_context():
    db.create_all()



if __name__ == '__main__':
    app.run(debug=True)