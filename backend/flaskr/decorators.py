import functools
import json
from functools import wraps
from flask import request, jsonify, current_app
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


def cache_response(timeout=60, persist=False):
    """
    A decorator to cache the response of a Flask view function.

    Args:
         timeout (int): Time in seconds to cache the result.
        persist (bool): If True, cache indefinitely unless explicitly invalidated.
    """

    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            redis_client = current_app.redis_client
            # Create a unique cache key using the request path, method, and query string
            cache_key = f"response_cache:{request.path}:{request.method}:{request.query_string.decode('utf-8')}"

            # Check if the response is in the cache
            cached_response = redis_client.get(cache_key) if redis_client else None
            if cached_response:
                print(f"Cache hit for {cache_key}")
                return jsonify(json.loads(cached_response))  # Convert back to JSON format

            print(f"Cache miss for {cache_key}. Processing request.")
            response = f(*args, **kwargs)

            # Cache the response
            if redis_client:
                if persist:
                    redis_client.set(cache_key, json.dumps(response.json))
                else:
                    redis_client.setex(cache_key, timeout, json.dumps(response.json))  # Cache the JSON response

            return response

        return wrapped

    return decorator
