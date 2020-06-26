from flask import jsonify

def wrap_response(data, msg, code):
    obj = {"msg": msg}
    if not data is None:
        if type(data) == list:
            obj["data"] = [dat.as_dict() for dat in data]
        else:
            obj["data"] = data.as_dict()
    return jsonify(obj), code
    