from flask import Flask
from flask.ext.httpauth import HTTPBasicAuth
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

    # Register middlewares here
    from application.middlewares import require_login
    app.before_request(require_login)

    # Register blueprints here
    from application.authorization.views import bp as bp_auth
    app.register_blueprint(bp_auth)

    return app
