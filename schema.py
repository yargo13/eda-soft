import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import Classroom as ClassroomModel
from models import School as SchoolModel
from models import User as UserModel
from models import Role as RoleModel
from models import School_Admin as School_AdminModel
from models import Teacher as TeacherModel
from models import Parent as ParentModel
from models import Student as StudentModel
from models import Questionnaire as QuestionnaireModel
from models import Questionnaire_Response as Questionnaire_ResponseModel
from models import Question as QuestionModel
from models import Question_Response as Question_ResponseModel
from database import db_session
from datetime import date
import ast

class Classroom(SQLAlchemyObjectType):
    class Meta:
        model = ClassroomModel

class School(SQLAlchemyObjectType):
    class Meta:
        model = SchoolModel

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

class Role(SQLAlchemyObjectType):
    class Meta:
        model = RoleModel

class School_Admin(SQLAlchemyObjectType):
    class Meta:
        model = School_AdminModel

class Teacher(SQLAlchemyObjectType):
    class Meta:
        model = TeacherModel

class Parent(SQLAlchemyObjectType):
    class Meta:
        model = ParentModel

class Student(SQLAlchemyObjectType):
    class Meta:
        model = StudentModel

class Questionnaire(SQLAlchemyObjectType):
    class Meta:
        model = QuestionnaireModel

class Questionnaire_Response(SQLAlchemyObjectType):
    class Meta:
        model = Questionnaire_ResponseModel

class Question(SQLAlchemyObjectType):
    class Meta:
        model = QuestionModel

class Question_Response(SQLAlchemyObjectType):
    class Meta:
        model = Question_ResponseModel

class Query(graphene.ObjectType):
    # Get a list of all chores
    get_questionnaires = graphene.List(Questionnaire, student_id=graphene.String())
    def resolve_get_questionnaires(self, info, **args):
        query = Questionnaire.get_query(info)
        student_id = args.get('student_id')
        student = StudentModel.query.filter(StudentModel.id == student_id).first()
        if student is not None:
            student_age = ((date.today() - student.birth_date).days)/365
            return query.filter(QuestionnaireModel.mininum_age <= student_age, QuestionnaireModel.maximum_age >= student_age).all()
        else:
            return None

    get_answers = graphene.List(Questionnaire_Response, student_id=graphene.Int())
    def resolve_get_answers(self, info, **args):
        query = Questionnaire_Response.get_query(info)
        student_id = args.get('student_id')
        student = StudentModel.query.filter(StudentModel.id == student_id).first()
        if student is not None:
            return query.filter(Questionnaire_ResponseModel.student == student, Questionnaire_ResponseModel.responses != None).all()
        else:
            return None

    get_answers_questionnaire = graphene.List(Questionnaire_Response, student_id=graphene.Int(), questionnaire_id = graphene.Int())
    def resolve_get_answers_questionnaire(self, info, student_id, questionnaire_id):
        query = Questionnaire_Response.get_query(info)
        student = StudentModel.query.filter(StudentModel.id == student_id).first()
        query = query.join()
        if student is not None:
            return query.filter(Questionnaire_ResponseModel.student == student,
            Questionnaire_ResponseModel.responses != None,
            Questionnaire_ResponseModel.responses.any(Question_ResponseModel.question.has(QuestionModel.questionnaire_id == questionnaire_id))).all()
        else:
            return None
        
    get_questionnaire = graphene.Field(Questionnaire, questionnaire_id = graphene.Int())
    def resolve_get_questionnaire(self, info, **args):
        query = Questionnaire.get_query(info)
        questionnaire_id = args.get('questionnaire_id')
        return query.filter(QuestionnaireModel.id == questionnaire_id).first()


    get_parent = graphene.Field(Parent, parent_id = graphene.Int())
    def resolve_get_parent(self, info, **args):
        query = Parent.get_query(info)
        parent_id = args.get('parent_id')
        return query.filter(ParentModel.id == parent_id).first()

    get_student = graphene.Field(Student, student_id = graphene.Int())
    def resolve_get_student(self, info, **args):
        query = Student.get_query(info)
        student_id = args.get('student_id')
        return query.filter(StudentModel.id == student_id).first()       


    get_children = graphene.List(Student, parent_id = graphene.Int())
    def resolve_get_children(self, info, **args):
        query = Student.get_query(info)
        parent_id = args.get('parent_id')
        return query.filter(StudentModel.parents.any(ParentModel.id == parent_id)).all()

    

class respondQuestionnaire(graphene.Mutation):
    class Arguments:
        student_id = graphene.Int()
        submitter_id = graphene.Int()
        questionnaire_id = graphene.Int()
        responses = graphene.String()
    ok = graphene.Boolean()
    def mutate(self, info, **args):
        student_id = args.get('student_id')
        submitter_id = args.get('submitter_id')
        questionnaire_id = args.get('questionnaire_id')
        student = StudentModel.query.filter(StudentModel.id == student_id).first()
        questionnaire = QuestionnaireModel.query.filter(QuestionnaireModel.id == questionnaire_id).first()
        submitter = UserModel.query.filter(UserModel.id == submitter_id).first()
        if student is not None and questionnaire is not None and submitter is not None:
            responses_json = args.get('responses')
            responses = ast.literal_eval(responses_json)
            questionnaire_response = Questionnaire_ResponseModel(student_id = student.id, submitter_id = submitter.id, questionnaire_id = questionnaire.id)
            db_session.add(questionnaire_response)
            db_session.commit()
            questionnaire_sum = 0
            for question_id in responses:
                question = QuestionModel.query.filter(QuestionModel.id == question_id).first()
                response = responses[question_id]
                question_response = Question_ResponseModel(question_id = question.id, response = response)
                questionnaire_response.responses.append(question_response)
                questionnaire_sum += int(response)
            if questionnaire_sum < questionnaire.lower_range:
                questionnaire_response.result = 'Baixo'
            elif questionnaire_sum < questionnaire.upper_range:
                questionnaire_response.result = 'Médio'
            else:
                questionnaire_response.result = 'Alto'
            db_session.commit()
            return respondQuestionnaire(ok = True)


class MyMutations(graphene.ObjectType):
    respond_questionnaire = respondQuestionnaire.Field()


schema = graphene.Schema(query=Query, mutation=MyMutations )
