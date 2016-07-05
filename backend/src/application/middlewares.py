"""
Middleware - piece of code launched before/after a request adding a functionality.
E.g. require api endpoints to pass only logged in users by default.

NOTE: A middleware written here must be explicitly added to `application.create_app` (__init__.py file).

Decorating middleware function with `@app.before_request` won't work if this file is not imported
anywhere in between `manage.py runserver` command and `manager.run()`.
So just to be safe, call `app.XXX_request(middleware_func)` in `create_app`.
"""
from flask import session, g


def check_valid_login():
    """
    Requires to be logged in.
    To make an endpoint public, use `public_endpoint` decorator.
    """
    import pdb
    pdb.set_trace()
    login_valid = 'user' in session  # or whatever you use to check valid login
    a = g.user
    #
    # if (request.endpoint and  'static' not in request.endpoint and
    #     not login_valid and
    #     not getattr(app.view_functions[request.endpoint], 'is_public', False) ) :
    #     return render_template('login.html', next=request.endpoint)
