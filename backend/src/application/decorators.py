def public_endpoint(function):
    """
    Makes endpoint usable for not logged in users.
    """
    function.is_public = True
    return function
