import base64
import calendar
import datetime
import hashlib
import hmac

import jwt
from flask import current_app, request
from flask_restx import abort

from project.exceptions import ItemNotFound


def generate_password_digest(password):
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )


def jwt_decode(token):
    try:
        decoded_jwt = jwt.decode(token, current_app.config["SECRET_KEY"], current_app.config["JWT_ALGORITHM"])
    except:
        return False
    else:
        return decoded_jwt


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, current_app.config["SECRET_KEY"], current_app.config["JWT_ALGORITHM"])
            decoded_token = jwt.decode(token, current_app.config["SECRET_KEY"], current_app.config["JWT_ALGORITHM"])
            user_id = decoded_token["id"]
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs, user_id_1=user_id)

    return wrapper


# def auth_required(func):
#     def wrapper(*args, **kwargs):
#         if  :
#             return func(*args, **kwargs)
#         abort(401, "Authorization Error")
#     return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        decoded_jwt = auth_check()
        if decoded_jwt:
            role = decoded_jwt.get("role")
            if role == "admin":
                return func(*args, **kwargs)
        abort(401, "Admin role required")
    return wrapper


def generate_token(data):
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, current_app.config["SECRET_KEY"], algorithm=current_app.config["JWT_ALGORITHM"])
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, current_app.config["SECRET_KEY"], algorithm=current_app.config["JWT_ALGORITHM"])
    return {'access_token': access_token, 'refresh_token': refresh_token}


def get_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode('utf-8'),
        salt=current_app.config['PWD_SALT'],
        iterations=current_app.config['PWD_ITERATIONS']
    )


def compare_password(hash_password, password):
    return hmac.compare_digest(
        base64.b64encode(hash_password),
        get_password_digest(password)
    )


def login_user(req_json, user):
    user_email = req_json.get("email")
    user_pass = req_json.get("password")
    if user_email and user_pass:
        pass_hashed = user["password"]
        req_json["role"] = user["role"]
        req_json["id"] = user["id"]
        if compare_password(pass_hashed, user_pass):
            return generate_token(req_json)
    raise ItemNotFound


def refresh_user_token(req_json):
    refresh_token = req_json.get("refresh_token")
    data = jwt_decode(refresh_token)
    if data:
        tokens = generate_token(data)
        return tokens
    raise ItemNotFound