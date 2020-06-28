from flask import jsonify, request

def wrap_response(data, msg, code):
    obj = {"msg": msg}
    if not data is None:
        if type(data) == list:
            obj["data"] = [dat.as_dict() for dat in data]
        else:
            obj["data"] = data.as_dict()
    return jsonify(obj), code

def body_required(fn):
    def wrapper(*args, **kwargs):
        if request.get_json() is None:
            return wrap_response(None, "Body Required", 400)
        else:
            return fn(*args, **kwargs)
    return wrapper
    