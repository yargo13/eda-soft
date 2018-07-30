from flask import Flask
from flask import render_template, abort, request, flash, redirect, json, url_for
from models import *
from database import db_session
from schema import schema
from datetime import date, datetime
import dateutil.parser
from flask_graphql import GraphQLView
from flask_migrate import Migrate
from requests import get, post
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'eda-enzo-luciana'
migrate = Migrate(app, db_session)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

app.add_url_rule(
    '/graphql',
    view_func = GraphQLView.as_view(
        'graphql',
        schema = schema,
        graphiql = True
    )
)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/parent/<id>/')
def parent(id=1):
    query = get('''http://localhost:5000/graphql?query={
        getParent(parentId:'''+id+'''){
            id,
            user {
                firstName
            }
            children {
                id, firstName
            }
        }
    }''').json()
    parent = query["data"]["getParent"]
    if parent is None:
        abort(404)
    else:
        return render_template('parent.html', parent=parent)

@app.route('/parent/<parent_id>/student/<student_id>/')
def student(parent_id, student_id):
    query_student = get('''http://localhost:5000/graphql?query={
        getStudent(studentId:'''+student_id+'''){
            id,
            firstName,
            surname,
            studentNumber,
            birthDate,
            questionnaireResponses {
                questionnaire {
                  id,
                  name
                }
            }
        }
    }''').json()
    student = query_student["data"]["getStudent"]
    birthDateString = student["birthDate"]
    birthDate = datetime.strptime(birthDateString, '%Y-%m-%d').date()
    student["birthDate"] = birthDate.strftime("%d/%m/%Y")
    questionnaires_answered = query_student["data"]["getStudent"]["questionnaireResponses"]
    ids = {}
    for answer in questionnaires_answered:
        if answer["questionnaire"]["id"] not in ids:
            ids[answer["questionnaire"]["id"]] = answer["questionnaire"]["name"]
    student["questionnairesAnswered"] = ids
    query_questionnaires = get('''http://localhost:5000/graphql?query={
        getQuestionnaires(studentId:"'''+student["id"]+'''"){
            id,
            name
        }
    }''').json()
    print(query_questionnaires)
    questionnaires = query_questionnaires["data"]["getQuestionnaires"]
    return render_template('student.html', parent_id = parent_id, student=student, questionnaires = questionnaires)

@app.route('/parent/<parent_id>/student/<student_id>/questionnaire/<questionnaire_id>/', methods = ["POST", "GET"])
def student_questionnaire(parent_id, student_id, questionnaire_id):
    if request.method == 'POST':
        query_parent = get('''http://localhost:5000/graphql?query={
            getParent(parentId:'''+parent_id+'''){
                user {
                    id
                }
            }
        }''').json()
        user_id = query_parent["data"]["getParent"]["user"]["id"]
        answers = json.dumps(request.form).replace('"','\\"')
        mutation = (post('http://localhost:5000/graphql', json={"query":'''mutation {
            respondQuestionnaire(studentId:'''+student_id+
                '''questionnaireId:'''+questionnaire_id+
                '''submitterId:'''+user_id+
                ''',responses:"'''+answers+'''"){
                ok
            }
        }'''}).json())
        print(mutation)
        if mutation["data"]["respondQuestionnaire"]["ok"] == True:
            return redirect(url_for('student', student_id = student_id, parent_id = parent_id), code = 302)
    query_questionnaire = get('''http://localhost:5000/graphql?query={
        getQuestionnaire(questionnaireId:'''+questionnaire_id+'''){
            name,
            questions{
                id,
                text
            }
        }
    }''').json()
    questionnaire = query_questionnaire["data"]["getQuestionnaire"]
    return render_template('student_questionnaire.html', student=student, questionnaire=questionnaire)

@app.route('/parent/<parent_id>/student/<student_id>/answers/<questionnaire_id>/')
def student_answers(parent_id, student_id, questionnaire_id):
    query_questionnaire = get('''http://localhost:5000/graphql?query={
        getQuestionnaire(questionnaireId:'''+questionnaire_id+'''){
            name,
        }
    }''').json()
    query_answers= get('''http://localhost:5000/graphql?query={
        getAnswersQuestionnaire(studentId:'''+student_id+''',questionnaireId:'''+questionnaire_id+'''){
            result,
            timestamp,
            submitter {
                firstName,
                surname
            }
        }
    }''').json()
    questionnaire = query_questionnaire["data"]["getQuestionnaire"]
    answers = query_answers["data"]["getAnswersQuestionnaire"]
    for answer in answers:
        timestamp = dateutil.parser.parse(answer["timestamp"])
        answer["timestamp"] = timestamp.strftime("%d/%m/%Y %H:%M")
    print(answers)
    return render_template('student_answers.html', questionnaire = questionnaire, answers = answers)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
