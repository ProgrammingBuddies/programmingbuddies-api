from flask import request, jsonify
from api import app
from api.controllers import projectController

# Project
@app.route("/projects", methods=['POST'])
def post_project():
    project = projectController.create_project(**request.get_json())

    if project == None:
        return "Failed to create project.", 400
    else:
        return jsonify(project.as_dict()), 201

@app.route("/projects/<id>", methods=['POST'])
def update_project(id):
    if 'id' in request.get_json():
        return "Failed to update project. Request body can not specify project's id.", 400

    project = projectController.update_project(id, **request.get_json())

    if project == None:
        return "Failed to update project.", 400
    else:
        return jsonify(project.as_dict()), 200

@app.route("/projects/<id>", methods=['GET'])
def get_project(id):
    project = projectController.get_project(id=id)

    if project:
        return jsonify(project.as_dict()), 200
    else:
        return "", 404

@app.route("/projects", methods=['GET'])
def get_all_projects():
    all_projects = projectController.get_all_projects()

    projects = [ project.as_dict() for project in all_projects ]

    return jsonify(projects), 200

@app.route("/projects/<id>", methods=['DELETE'])
def delete_project(id):
    project = projectController.delete_project(id)

    if project:
        return "", 202
    else:
        return "", 404

# Project Link
@app.route("/projects/<project_id>/links", methods=['POST'])
def create_project_link(project_id):
    if 'project_id' in request.get_json():
        return "Failed to create project link. Request body can not specify link's project_id.", 400

    link = projectController.create_link(project_id, **request.get_json())

    if link == None:
        return "Failed to create project link.", 400
    else:
        return jsonify(link.as_dict()), 201

@app.route("/projects/<project_id>/links/<link_id>", methods=['POST'])
def update_project_link(project_id, link_id):
    if 'project_id' in request.get_json():
        return "Failed to update project link. Request body can not specify link's project_id.", 400
    elif 'link_id' in request.get_json():
        return "Failed to update project link. Request body can not specify link's link_id.", 400

    link = projectController.update_link(project_id, link_id, **request.get_json())

    if link == None:
        return "Failed to update project link.", 400
    else:
        return jsonify(link.as_dict()), 200

@app.route("/projects/<project_id>/links", methods=['GET'])
def get_all_project_links(project_id):
    all_links = projectController.get_all_links(project_id)

    links = [ link.as_dict() for link in all_links ]

    return jsonify(links), 200

@app.route("/projects/<project_id>/links/<link_id>", methods=['DELETE'])
def delete_project_link(project_id, link_id):
    link = projectController.delete_link(project_id, link_id)

    if link == None:
        return "", 404
    else:
        return "", 200

# Project Feedback
@app.route("/projects/<project_id>/feedbacks", methods=['POST'])
def create_project_feedback(project_id):
    if 'project_id' in request.get_json():
        return "Failed to create feedback. Request body can not specify feedback's project_id.", 400

    feedback = projectController.create_feedback(project_id, **request.get_json())

    if feedback == None:
        return "Failed to create feedback.", 400
    else:
        return jsonify(feedback.as_dict()), 201

@app.route("/projects/<project_id>/feedbacks", methods=['GET'])
def get_all_project_feedbacks(project_id):
    all_feedbacks = projectController.get_all_feedbacks(project_id)

    feedbacks = [ feedback.as_dict() for feedback in all_feedbacks ]

    return jsonify(feedbacks), 200

@app.route("/projects/<project_id>/feedbacks/<feedback_id>", methods=['DELETE'])
def delete_project_feedback(project_id, feedback_id):
    feedback = projectController.delete_feedback(project_id, feedback_id)

    if feedback == None:
        return "", 404
    else:
        return "", 200
