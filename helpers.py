from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from models import User


def role_required(allowed_roles):
    """
    Use as:
    @role_required(["admin", "owner"])
    def some_route(): ...
    """

    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            role = identity.get("role")
            if role not in allowed_roles:
                return jsonify({"message": "Forbidden: insufficient role"}), 403
            return fn(*args, **kwargs)

        return decorated

    return wrapper


def get_current_user():
    verify_jwt_in_request()
    identity = get_jwt_identity()
    user_id = identity.get("id")
    user = User.query.get(user_id)
    return user