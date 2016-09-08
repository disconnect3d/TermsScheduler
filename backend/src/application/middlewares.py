"""
Middleware - piece of code launched before/after a request adding a functionality.
E.g. require api endpoints to pass only logged in users by default.

NOTE: A middleware written here must be explicitly added to `application.create_app` (__init__.py file).

Decorating middleware function with `@app.before_request` won't work if this file is not imported
anywhere in between `manage.py runserver` command and `manager.run()`.
So just to be safe, call `app.XXX_request(middleware_func)` in `create_app`.
"""
from flask import current_app, request, g
from flask.ext.restful import abort

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
    if request.endpoint and 'static' not in request.endpoint:
        is_admin_site = request.endpoint.startswith('admin.')

        endpoint = current_app.view_functions.get(request.endpoint, None)

        if hasattr(endpoint, 'view_class'):  # Checking for `is_public` in a `restful.Resource` API method
            method_func = getattr(endpoint.view_class, request.method.lower(), None)
            is_public_url = getattr(method_func, 'is_public', False)
        else:
            is_public_url = getattr(endpoint, 'is_public', False)

        if not is_public_url:
            authorization = _check_auth()

            # if the user is logged in and he is not admin, kick him out off admin sites
            if is_admin_site and (hasattr(g, 'user') and not g.user.is_admin):
                abort(401)

            return authorization


def apply_cors_headers(response):
    """
    Plain CORS implementation. The `Allow-Methods` should be somehow dynamic. # TODO/FIXME
    Didn't use Flask-Cors or Flask-Restful cors because it ... didn't work.

    Tested on code:
        * Flask-Restful:
            api.decorators = [
                cors.crossdomain(
                    origin=app.config['CORS_ORIGINS'],
                    methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS'],
                    attach_to_all=True,
                    automatic_options=True
                )
            ]

        * Flask-Cors:
            CORS(app, resources={r"*": {"origins": app.config['CORS_ORIGINS']}})
    """
    response.headers.add('Access-Control-Allow-Origin', current_app.config['CORS_ORIGINS'])
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
