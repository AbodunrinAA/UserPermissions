from werkzeug.security import safe_str_cmp
from Models.UserModel import UserModel


def authenticate(username, password):
    user = UserModel.getUser_By_Username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):  # unique to Flask-JWT
    user_id = payload['identity']
    return UserModel.getUser_By_Id(user_id)


secrete_key = '$$$Ademola@#'


