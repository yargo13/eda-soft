from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eda.db'
db = SQLAlchemy(app)

class Student(db.Model):
    studentId = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), unique = True, nullable = False)
    middleName = db.Column(db.String(30), unique = False, nullable = True)
    lastName = db.Column(db.String(30), unique = False, nullable = False)
    birth = db.Column(db.Date(), unique = False, nullable = False)

    def __repr__(self):
        return '<Recipe %r>' % self.title