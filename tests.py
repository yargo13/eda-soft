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

    enzo = Student(first_name = 'Enzo', surname = 'Rossi', birth_date = date(2018,5,15), gender = 'm', height = 0.38, weight = 13,  student_number = '20180001')
    valentina = Student(first_name = 'Valentina', surname = 'Mattos', birth_date = date(2017,11,19), gender = 'f', height = 0.51, weight = 17,  student_number = '20180002')
    db_session.add(enzo)
    db_session.add(valentina)
    db_session.commit()

    parent_luciana.children.append(enzo)
    maternal1.students.append(enzo)
    maternal1.students.append(valentina)
    db_session.commit()

    questionnaire1 = Questionnaire(mininum_age = 1/12, maximum_age = 3/12, lower_range = 22.5, upper_range = 35, name = "Questionário de Comunicação")
    questionnaire2 = Questionnaire(mininum_age = 1/12, maximum_age = 3/12, lower_range = 42.5, upper_range = 47.5, name = "Questionário de Coordenação Motora Ampla")
    questionnaire3 = Questionnaire(mininum_age = 1/12, maximum_age = 3/12, lower_range = 32.5, upper_range = 37.5, name = "Questionário de Coordenação Motora Fina")
    questionnaire4 = Questionnaire(mininum_age = 1/12, maximum_age = 3/12, lower_range = 22.5, upper_range = 37.5, name = "Questionário de Resolução de Problemas")
    questionnaire5 = Questionnaire(mininum_age = 1/12, maximum_age = 3/12, lower_range = 32.5, upper_range = 42.5, name = "Questionário Pessoal-Social")
    db_session.add(questionnaire1)
    db_session.add(questionnaire2)
    db_session.add(questionnaire3)
    db_session.add(questionnaire4)
    db_session.add(questionnaire5)
    db_session.commit()
    
    questionnaire1.questions.append(Question(text = "Seu bebê às vezes faz sons com a garganta que parecem com um gargarejo?"))
    questionnaire1.questions.append(Question(text = "Seu bebê faz sons como “ooo”, “gah” e “aah”?"))
    questionnaire1.questions.append(Question(text = "Quando você fala com seu bebê, ela faz sons de volta para você?"))
    questionnaire1.questions.append(Question(text = "Seu bebê sorri quando você fala com ele?"))
    questionnaire1.questions.append(Question(text = "Seu bebê ri baixinho/suavemente?"))
    questionnaire1.questions.append(Question(text = "Depois de ter ficado fora de vista, o seu bebé sorri ou fica excitado quando o vê?"))
    questionnaire2.questions.append(Question(text = "Enquanto seu bebê está de costas, ele acena com os braços e pernas, mexe e se contorce?"))
    questionnaire2.questions.append(Question(text = "Quando seu bebê está em sua barriga, ela vira a cabeça para o lado?"))
    questionnaire2.questions.append(Question(text = "Quando seu bebê está de bruços, ele segura a cabeça mais do que alguns segundos?"))
    questionnaire2.questions.append(Question(text = "Quando seu bebê está de costas, ela chuta as pernas?"))
    questionnaire2.questions.append(Question(text = "Enquanto seu bebê está de costas, ele move a cabeça de um lado para o outro?"))
    questionnaire2.questions.append(Question(text = "Depois de segurar a cabeça do bebê enquanto em sua barriga, seu bebê a coloca voltar para o chão, em vez de deixá-lo cair ou cair para frente?"))
    questionnaire3.questions.append(Question(text = "A mão do seu bebê geralmente está bem fechada quando ele está acordado? (Se seu bebê costumava fazer isso, mas não faz mais, marque \"sim\".)"))
    questionnaire3.questions.append(Question(text = "Seu bebê agarra seu dedo se você tocar a palma da mão dele?"))
    questionnaire3.questions.append(Question(text = "Quando você coloca um brinquedo na mão, seu bebê o segura na mão brevemente?"))
    questionnaire3.questions.append(Question(text = "Seu bebê toca seu rosto com as mãos?"))
    questionnaire3.questions.append(Question(text = "Seu bebê mantém as mãos abertas ou parcialmente abertas quando ele está acordado (ao invés de em punhos, como eles estavam quando ele estava um recém-nascido)?"))
    questionnaire3.questions.append(Question(text = "Seu bebê pega ou arranha suas roupas?"))
    questionnaire4.questions.append(Question(text = "Seu bebê olha para objetos que estão a 20-25 centimetros de distância?"))
    questionnaire4.questions.append(Question(text = "Quando você se movimenta, o seu bebê segue você com os olhos?"))
    questionnaire4.questions.append(Question(text = "Quando você move um brinquedo lentamente de um lado para o outro em frente à cara do bebê (cerca de 10 centímetros de distância), o seu bebê segue o brinquedo com os olhos, às vezes virando a cabeça?"))
    questionnaire4.questions.append(Question(text = "Quando você move um pequeno brinquedo para cima e para baixo lentamente na frente da cara do bebê (cerca de 10 centímetros de distância), o seu bebê segue o brinquedo com os olhos?"))
    questionnaire4.questions.append(Question(text = "Quando você segura seu bebê sentado, ele olha para um brinquedo (mais ou menos o tamanho de um copo ou chocalho) que você coloca na mesa ou no chão frente dele?"))
    questionnaire4.questions.append(Question(text = "Quando você balança um brinquedo acima do seu bebê enquanto ele está deitado de costas, ele acena com os braços para o brinquedo ?"))
    questionnaire5.questions.append(Question(text = "Seu bebê às vezes tenta sugar, mesmo quando ela não está se alimentando?"))
    questionnaire5.questions.append(Question(text = "Seu bebê chora quando está com fome, molhado, cansado ou quer ser segurado?"))
    questionnaire5.questions.append(Question(text = "Seu bebê sorri para você?"))
    questionnaire5.questions.append(Question(text = "Quando você sorri para seu bebê, ela sorri de volta?"))
    questionnaire5.questions.append(Question(text = "O seu bebê observa as mãos dele?"))
    questionnaire5.questions.append(Question(text = "Quando seu bebê vê a mama ou a mamadeira, ele parece saber que está prestes a ser alimentado?"))
    db_session.commit()
    

from requests import put, get, delete

init_db()

print(Classroom.query.first().students)

print(Teacher.query.first().user)

print(Parent.query.first().user)