from sqlalchemy import *
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key = True)
    first_name = Column(String(20), nullable = False)
    surname = Column(String(50), nullable = False)
    birth_date = Column(Date, nullable = False)
    classroom_id = Column(Integer, ForeignKey('classroom.id'), nullable = False)
    student_number = Column(String(20), nullable = False)
    gender = Column(String(1), nullable = False)

    def __repr__(self):
        return '<Student %r %r>' % (self.first_name, self.surname)

class Classroom(Base):
    __tablename__ = 'classroom'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    school_id = Column(Integer, ForeignKey('school.id'), nullable = False)
    teacher_id = Column(Integer, ForeignKey('teacher.id'), nullable = False)
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
    role_id = Column(Integer, ForeignKey('role.id'), default = 3, nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'), unique = True, nullable = False)

class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer, primary_key = True)
    role_id = Column(Integer, ForeignKey('role.id'), default = 3, nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'), unique = True, nullable = False)

class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key = True)
    role_id = Column(Integer, ForeignKey('role.id'), default = 4, nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'), unique = True, nullable = False)

class Family(Base):
    __tablename__ = 'family'
    id = Column(Integer, primary_key = True)
    parent_id = Column(Integer, ForeignKey('parent.id'), nullable = False)
    student_id = Column(Integer, ForeignKey('student.id'), nullable = False)
