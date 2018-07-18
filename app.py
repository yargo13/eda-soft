from flask import Flask
from database import db_session
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug = True)
