from flask import jsonify

def fail(msg, code=400):
    return jsonify({"status": "failed", "msg": msg}), int(code)

def success(data, code=200):
    return jsonify({"status": "success", "data": data}), int(code)