from flask import jsonify, request
from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from api.controllers import userController
def wrap_response(data, msg, code):
    obj = {"msg": msg}
    if not data is None:
        if type(data) == list:
            obj["data"] = [dat.as_dict() for dat in data]
        else:
            obj["data"] = data.as_dict()
    return jsonify(obj), code

def body_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if request.get_json() is None:
            return wrap_response(None, "Body Required", 400)
        else:
            return fn(*args, **kwargs)
    return wrapper
    
def verify_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print("!")
        verify_jwt_in_request()
        print("§")
        user, msg, code = userController.get_user_from_jwt()
        if user is None:
            return wrap_response(user, msg, code)
        else:
            return fn(*args, **kwargs)
    return wrapper