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
from models import Questionnaire_Answer as Questionnaire_AnswerModel
from models import Question as QuestionModel
from models import Question_Answer as Question_AnswerModel
from database import db_session

class Todo(SQLAlchemyObjectType):
    class Meta:
        model = TodoModel

class Person(SQLAlchemyObjectType):
    class Meta:
        model = PersonModel

# Create a Todo
class createTodo(graphene.Mutation):

    class Arguments:
        item = graphene.String()
        person = graphene.String()
    ok = graphene.Boolean()
    todo = graphene.Field(Todo)

    def mutate(self, info, **args):
        item = args.get('item')
        person = args.get('person')
        person_query = PersonModel.query.filter(PersonModel.name==person).first()
        if person_query is None:
            return createTodo(todo = None, ok = False)
        else:
            person_id = person_query.id
            todo = TodoModel(item=item,person_id=person_id)
            db_session.add(todo)
            db_session.commit()
            return createTodo(todo = todo, ok = True)

# Delete one Todo by its item
class deleteTodo(graphene.Mutation):
    class Arguments:
        item = graphene.String()
    ok = graphene.Boolean()

    def mutate(self, info, **args):
        item = args.get('item')
        item_query = TodoModel.query.filter(TodoModel.item == item).first()
        if item_query is None:
            return deleteTodo(ok = False)
        else:
            db_session.delete(item_query)
            db_session.commit()
            return createTodo(ok = True)

# Update de person doing a Todo
class updateTodo(graphene.Mutation):
    class Arguments:
        item = graphene.String()
        person = graphene.String()
    ok = graphene.Boolean()
    todo = graphene.Field(Todo)

    def mutate(self, info, **args):
        item = args.get('item')
        person = args.get('person')
        item_query = TodoModel.query.filter(TodoModel.item == item).first()
        if item_query is None:
            return updateTodo(todo = None, ok = false)
        else:
            person_query = PersonModel.query.filter(PersonModel.name==person).first()       
            if person_query is None:
                return updateTodo(todo = None, ok = False)
            else:
                person_id = person_query.id
                item_query.person_id = person_id
                db_session.commit()
                return updateTodo(todo = item_query, ok = True)

class Query(graphene.ObjectType):
    # Get a list of all chores
    all_todos = graphene.List(Todo)
    def resolve_all_todos(self, info, **args):
        query = Todo.get_query(info)
        return query.all()
    
    # Get chores separated by person and can search for a specific one
    get_chores = graphene.List(Person, person=graphene.String())
    def resolve_get_chores(self, info, **args):
        query = Person.get_query(info)
        person = args.get('person')
        if person is not None:
            return query.filter(PersonModel.name == person).all()
        else:
            return query.all()

class MyMutations(graphene.ObjectType):
    create_todo = createTodo.Field()
    delete_todo = deleteTodo.Field()
    update_todo = updateTodo.Field()

schema = graphene.Schema(query=Query,mutation=MyMutations)
