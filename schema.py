import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from models import Student as StudentModel
from database import db_session

class Student(SQLAlchemyObjectType):
    class Meta:
        model = StudentModel

class Query(graphene.ObjectType):
    students = graphene.List(Student)

    def resolve_students(self, info):
        query = Student.get_query(info)
        return query.all()

schema = graphene.Schema(query=Query)
