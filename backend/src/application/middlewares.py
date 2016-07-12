"""
Middleware - piece of code launched before/after a request adding a functionality.
E.g. require api endpoints to pass only logged in users by default.

NOTE: A middleware written here must be explicitly added to `application.create_app` (__init__.py file).

Decorating middleware function with `@app.before_request` won't work if this file is not imported
anywhere in between `manage.py runserver` command and `manager.run()`.
So just to be safe, call `app.XXX_request(middleware_func)` in `create_app`.
"""

from application import auth


@auth.login_required
def require_login():
    """
    Requires to be logged in.
    To make an endpoint public, use `public_endpoint` decorator.
    """
    # The `@auth.login_required` decoration is enough to make it require login.
    pass
