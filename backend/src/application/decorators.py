from functools import wraps

from flask import g
from flask.ext.restful import abort


def public_endpoint(function):
    """
    Makes endpoint usable for not logged in users.
    """
    function.is_public = True
    return function


def require_admin(function):
    """
    Wraps endpoint so that it returns UNAUTHORIZED if user is not an admin.
    """
    @wraps(function)
    def decorated(*args, **kwargs):
        if g.user.is_admin:
            return function(*args, **kwargs)
        else:
            abort(401)

    return decorated
