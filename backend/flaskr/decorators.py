from functools import wraps
from flask_jwt_extended import jwt_required


def swagger_doc(description, parameters=None, responses=None):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Add OpenAPI documentation details
        if not hasattr(wrapper, '_apidoc'):
            wrapper._apidoc = {}
        wrapper._apidoc['summary'] = description
        wrapper._apidoc['parameters'] = parameters or []
        wrapper._apidoc['responses'] = responses or {}

        return wrapper
    return decorator
