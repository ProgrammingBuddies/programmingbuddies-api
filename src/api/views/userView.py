from flask import request, jsonify
from api import app
from api.controllers import userController

# User
@app.route("/users", methods=['POST'])
def create_user():
    user = userController.create_user(**request.get_json())

    if user == None:
        return "Failed to create user.", 400
    else:
        return jsonify(user.as_dict()), 201

@app.route("/users/<id>", methods=['POST'])
def update_user(id):
    if 'id' in request.get_json():
        return "Failed to update user. Request body can not specify user id.", 400

    user = userController.update_user(id, **request.get_json())

    if user == None:
        return "Failed to update user.", 400
    else:
        return jsonify(user.as_dict()), 200

@app.route("/users/<id>", methods=['GET'])
def get_user(id):
    user = userController.get_user(id=id)

    if user:
        return jsonify(user.as_dict()), 200
    else:
        return "", 404

@app.route("/users", methods=['GET'])
def get_all_users():
    all_users = userController.get_all_users()

    users = [ user.as_dict() for user in all_users ]

    return jsonify(users), 200

@app.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
    user = userController.delete_user(id)

    if user:
        return "", 200
    else:
        return "", 404

# User Link
@app.route("/users/<user_id>/links", methods=['POST'])
def create_user_link(user_id):
    if 'user_id' in request.get_json():
        return "Failed to create link. Request body can not specify link's user_id.", 400

    link = userController.create_link(user_id, **request.get_json())

    if link == None:
        return "Failed to create link", 400
    else:
        return jsonify(link.as_dict()), 201

@app.route("/users/<user_id>/links/<link_id>", methods=['POST'])
def update_user_link(user_id, link_id):
    if 'user_id' in request.get_json():
        return "Failed to update user link. Request body can not specify link's user_id.", 400
    elif 'link_id' in request.get_json():
        return "Failed to update user link. Request body can not specify link's link_id.", 400

    link = userController.update_link(user_id, link_id, **request.get_json())

    if link == None:
        return "Failed to update user.", 400
    else:
        return jsonify(link.as_dict()), 200

@app.route("/users/<user_id>/links", methods=['GET'])
def get_all_user_links(user_id):
    all_links = userController.get_all_links(user_id)

    links = [ link.as_dict() for link in all_links ]

    return jsonify(links), 200

@app.route("/users/<user_id>/links/<link_id>", methods=['DELETE'])
def delete_user_link(user_id, link_id):
    link = userController.delete_link(user_id, link_id)

    if link == None:
        return "", 404
    else:
        return "", 200

# User Feedback
@app.route("/users/<user_id>/feedbacks", methods=['POST'])
def create_user_feedback(user_id):
    if 'user_id' in request.get_json():
        return "Failed to create feedback. Request body can not specify feedback's user_id.", 400

    feedback = userController.create_feedback(user_id, **request.get_json())

    if feedback == None:
        return "Failed to create feedback", 400
    else:
        return jsonify(feedback.as_dict()), 201

@app.route("/users/<user_id>/feedbacks", methods=['GET'])
def get_all_user_feedbacks(user_id):
    all_feedbacks = userController.get_all_feedbacks(user_id)

    feedbacks = [ feedback.as_dict() for feedback in all_feedbacks ]

    return jsonify(feedbacks), 200

@app.route("/users/<user_id>/feedbacks/<feedback_id>", methods=['DELETE'])
def delete_user_feedback(user_id, feedback_id):
    feedback = userController.delete_feedback(user_id, feedback_id)

    if feedback == None:
        return "", 404
    else:
        return "", 200
