from flask import Flask
from database import db_session
from flask_graphql import GraphQLView
from schema import schema
import os
from flask_migrate import Migrate

app = Flask(__name__)
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
