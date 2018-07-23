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
    get_questionnaires = graphene.List(Questionnaire, student_number=graphene.String())
    def resolve_get_questionnaires(self, info, **args):
        query = Questionnaire.get_query(info)
        student_number = args.get('student_number')
        if student_number is not None:
            student = StudentModel.query.filter(StudentModel.student_number == student_number).first()
            student_age = ((date.today() - student.birth_date).days)/365
            return query.filter(QuestionnaireModel.mininum_age <= student_age, QuestionnaireModel.maximum_age >= student_age).all()
        else:
            return None

class respondQuestionnaire(graphene.Mutation):
    class Arguments:
        student_number = graphene.String()
        responses = graphene.JSONString()
    ok = graphene.Boolean()
    def mutate(self, info, **args):
        student_number = args.get('student_number')
        student = StudentModel.query.filter(StudentModel.student_number == student_number).first()
        if student is not None:
            responses = args.get('responses')
            print(responses)
            questionnaire_response = Questionnaire_ResponseModel(student_id = student.id)
            db_session.add(questionnaire_response)
            db_session.commit()
            for question_id in responses:
                question = QuestionModel.query.filter(QuestionModel.id == question_id).first()
                question_response = Question_ResponseModel(question_id = question.id, response = responses[question_id])
                questionnaire_response.responses.append(question_response)
            db_session.commit()
            return respondQuestionnaire(ok = True)

class MyMutations(graphene.ObjectType):
    respond_questionnaire = respondQuestionnaire.Field()


schema = graphene.Schema(query=Query, mutation=MyMutations )
