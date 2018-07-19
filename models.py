from sqlalchemy import *
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Classroom(Base):
    __tablename__ = 'classroom'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    school_id = Column(Integer, ForeignKey('school.id'))
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    students = relationship('Student', backref='classroom', lazy=True)

class School(Base):
    __tablename__ = 'school'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    classrooms = relationship('Classroom', backref='school', lazy = True)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    first_name = Column(String(20), nullable = False)
    surname = Column(String(50), nullable = False)
    email = Column(String(128), unique = True, nullable = False)
    password = Column(String(128), nullable = False)
    telephone_number = Column(String(30))

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key = True)
    description = Column(String(10), unique = True)

class School_Admin(Base):
    __tablename__ = 'school_admin'
    id = Column(Integer, primary_key = True)
    role_id = Column(Integer, ForeignKey('role.id'), default = 3)
    user_id = Column(Integer, ForeignKey('user.id'), unique = True)

class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key = True)
    role_id = Column(Integer, ForeignKey('role.id'), default = 3)
    user_id = Column(Integer, ForeignKey('user.id'), unique = True)

family = Table(
    'family',
    Base.metadata,
    Column('parent_id', Integer, ForeignKey('parent.id')),
    Column('student_id', Integer, ForeignKey('student.id'))
)

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key = True)
    role_id = Column(Integer, ForeignKey('role.id'), default = 4)
    user_id = Column(Integer, ForeignKey('user.id'), unique = True)
    children = relationship("Student", secondary=family)

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key = True)
    first_name = Column(String(20), nullable = False)
    surname = Column(String(50), nullable = False)
    birth_date = Column(Date, nullable = False)
    classroom_id = Column(Integer, ForeignKey('classroom.id'))
    student_number = Column(String(20), nullable = False)
    gender = Column(String(1), nullable = False)
    parents = relationship("Parent", secondary=family)

    def __repr__(self):
        return '<Student %r %r>' % (self.first_name, self.surname)

class Questionnaire(Base):
    __tablename__ = 'questionnaire'
    id = Column(Integer, primary_key = True)
    mininum_age = Column(Float)
    maximum_age = Column(Float)

class Questionnaire_Answer(Base):
    __tablename__ = 'questionnaire_answer'
    id = Column(Integer, primary_key = True)
    student_id = Column(Integer, ForeignKey('student.id'))
    timestamp = Column(DateTime, default = datetime.now())

class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key = True)
    questionnaire_id = Column(Integer, ForeignKey('questionnaire.id'))
    text = Column(String(1000), nullable = False)

class Question_Answer(Base):
    __tablename__ = 'question_answer'
    id = Column(Integer, primary_key = True)
    questionnaire_answer_id = Column(Integer, ForeignKey('questionnaire_answer.id'))
    question_id = Column(Integer, ForeignKey('question.id'))
    answer = Column(String(256), nullable = False)



