from flask import jsonify

def fail(msg, code=400):
    return {"status": "failed", "msg": msg}, int(code)

def success(data, code=200):
    return {"status": "success", "data": data}, int(code)

def jsonify_response(data, code):
    return jsonify(data), code