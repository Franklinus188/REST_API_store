from hmac import compare_digest  # from werkzeug.security import safe_str_cmp (safe_str_cmp was removed in python 3.9)
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and compare_digest(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
