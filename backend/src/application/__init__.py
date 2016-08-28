from flask import Flask
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
auth = HTTPBasicAuth()


def create_app(config):
    """
    Application Factories - http://flask.pocoo.org/docs/patterns/appfactories/
    :param config: Path to config.py file.
    """

    app = Flask(__name__)
    app.config.from_pyfile(config)
    db.init_app(app)
    api = Api(app)

    from application.json_encoder import AlchemyEncoder
    app.json_encoder = AlchemyEncoder

    # Register middlewares here
    from application.middlewares import require_login
    app.before_request(require_login)

    # Register blueprints here
    from application.views import bp as bp_auth
    app.register_blueprint(bp_auth)

    from application.views import UserList, UserResource, GroupList, SubjectList, SubjectSignupList, \
        SubjectSignupResource
    api.add_resource(UserList, '/api/users')
    api.add_resource(UserResource, '/api/users/<int:id>')
    api.add_resource(GroupList, '/api/groups')
    api.add_resource(SubjectList, '/api/subjects')
    api.add_resource(SubjectSignupList, '/api/subjects_signup')
    api.add_resource(SubjectSignupResource, '/api/subjets_signup/<int:subject_id>')

    # Admin panel
    from application.models import User, Group
    from application.admin import UserAdminView

    admin = Admin(app)
    admin.add_view(UserAdminView(User, db.session))
    admin.add_view(ModelView(Group, db.session))

    return app
