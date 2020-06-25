from flask import jsonify

def wrap_response(data, msg, code):
    obj = {"msg": msg}
    if not data is None:
        obj["data"] = data.as_dict()
    return jsonify(obj), code
    