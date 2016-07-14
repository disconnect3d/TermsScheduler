"""
Middleware - piece of code launched before/after a request adding a functionality.
E.g. require api endpoints to pass only logged in users by default.

NOTE: A middleware written here must be explicitly added to `application.create_app` (__init__.py file).

Decorating middleware function with `@app.before_request` won't work if this file is not imported
anywhere in between `manage.py runserver` command and `manager.run()`.
So just to be safe, call `app.XXX_request(middleware_func)` in `create_app`.
"""
from flask import current_app, request

from application import auth


def _require_login_impl():
    pass

# Because the `auth.login_required` is a function decorator,
# and the proper logic lies in the wrapping function, it has to be done as it is ...
_check_auth = auth.login_required(_require_login_impl)


def require_login():
    """
    Requires to be logged in.
    To make an endpoint public, use `public_endpoint` decorator.
    """
    if not getattr(current_app.view_functions.get(request.endpoint, None), 'is_public', False):
        return _check_auth()
