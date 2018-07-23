#-*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from models import *
from database import Base, engine, db_session
from datetime import date

def init_db():
    Base.metadata.drop_all(bind = engine)
    Base.metadata.create_all(bind = engine)
    db_session.commit()

    system_admin = Role(description = 'system_admin')
    school_admin = Role(description = 'school_admin')
    teacher = Role(description = 'teacher')
    parent = Role(description = 'parent')
    db_session.add(system_admin)
    db_session.add(school_admin)
    db_session.add(teacher)
    db_session.add(parent)
    db_session.commit()

    escolinha1 = School(name = 'Escolinha 1')
    db_session.add(escolinha1)

    claudia = User(first_name = 'Claudia', surname = 'Pereira', email = 'claudia.pereira@gmail.com', password = '1234', telephone_number = '11912345678')
    luciana = User(first_name = 'Luciana', surname = 'Rossi', email = 'luciana.rossi@gmail.com', password = '1234', telephone_number = '11923456789')
    db_session.add(claudia)
    db_session.add(luciana)
    db_session.commit()
    
    teacher_claudia = Teacher(role_id = teacher.id, user_id = claudia.id)
    parent_luciana = Parent(role_id = parent.id, user_id = luciana.id)
    db_session.add(teacher_claudia)
    db_session.add(parent_luciana)
    db_session.commit()

    maternal1 = Classroom(name = 'Maternal 1', teacher_id = teacher_claudia.id, school_id = escolinha1.id)
    db_session.add(maternal1)
    db_session.commit()

    enzo = Student(first_name = 'Enzo', surname = 'Rossi', birth_date = date(2018,5,15), gender = 'm', student_number = '20180001')
    valentina = Student(first_name = 'Valentina', surname = 'Mattos', birth_date = date(2017,11,19), gender = 'f', student_number = '20180002')
    db_session.add(enzo)
    db_session.add(valentina)
    db_session.commit()

    parent_luciana.children.append(enzo)
    maternal1.students.append(enzo)
    maternal1.students.append(valentina)
    db_session.commit()

    questionnaire = Questionnaire(mininum_age = 0, maximum_age = 0.25)
    db_session.add(questionnaire)
    db_session.commit()
    
    question1 = Question(questionnaire_id = questionnaire.id, text = 'A criança olha diretamente na direção de quem fala?')
    enzo_answer = Questionnaire_Response(student_id = enzo.id)
    db_session.add(enzo_answer)
    db_session.add(question1)
    db_session.commit()

    question1_anwer = Question_Response(questionnaire_response_id = enzo_answer.id, question_id = question1.id, response = 'y')
    db_session.add(question1_anwer)
    db_session.commit()
    

from requests import put, get, delete

init_db()

print(Classroom.query.first().students)
