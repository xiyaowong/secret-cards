from functools import wraps

from flask import g, request

from back_end.models import User
from back_end.api.errors import error_response


def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("authorization", "")  # type: str
        print(token)
        if not token:
            return error_response(401)
        data = User.verify_token(token)
        if not data:
            return error_response(401)
        id = data.get("id")
        print(id)
        user = User.query.get_or_404(id)
        g.current_user = user
        return f(*args, **kwargs)
    return wrapper