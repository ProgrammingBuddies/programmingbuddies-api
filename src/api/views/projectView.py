from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from api import app
from api.utils import wrap_response, body_required
from api.controllers import projectController

# Project
@app.route("/project", methods=['POST'])
@jwt_required
@body_required
def create_project():
    """
    Create project
    Current user creates project
    ---
    tags:
        - Project
    parameters:
        -   in: body
            name: Project
            required: true
            description: Project object containing data for creation
            schema:
                $ref: "#/definitions/Project"
    definitions:
        - schema:
            id: Project
            properties:
                id:
                    type: integer
                    description: Id of the project. This property will be assigned a value returned by the database
                name:
                    type: string
                    description: Name of the project
                description:
                    type: string
                    description: Description of the project
                languages:
                    type: string
                    description: (Optional) List of programming languages the project uses
                development_status:
                    type: integer
                    description: Development status of the project
                creation_date:
                    type: string
                    description: (Optional) Creation date of the project
                release_date:
                    type: string
                    description: (Optional) Release date of the project
                repository:
                    type: string
                    description: Url of the project's repository
                users:
                    type: array
                    description: List of members of the project
                    items:
                        $ref: "#/definitions/User"
                links:
                    type: array
                    description: List of links
                    items:
                        $ref: "#/definitions/ProjectLink"
                feedbacks:
                    type: array
                    description: List of feedbacks given to the project
                    items:
                        $ref: "#/definitions/ProjectFeedback"
    responses:
        201:
            description: Project created successfully
        400:
            description: Failed to create project
        404:
            description: User doesn't exist
    """
    return wrap_response(*projectController.create_project(user_id=get_jwt_identity(), **request.get_json()))

@app.route("/project", methods=['PUT'])
@jwt_required
@body_required
def update_project():
    """
    Update project
    Updates current user's project with the data in request body
    ---
    tags:
        - Project
    parameters:
        -   in: body
            name: Project
            required: true
            description: Project object containing data to update
            schema:
                $ref: "#/definitions/Project"
    responses:
        200:
            description: Project updated successfully
        400:
            description: Failed to update project
        404:
            description: Current user or requested project not found
    """
    if "user_id" in request.get_json():
        return wrap_response(None, "Failed to update project. Request body must not contain 'user_id'.", 400)

    return wrap_response(*projectController.update_project(user_id=get_jwt_identity(), **request.get_json()))

@app.route("/projects/<id>", methods=['GET'])
def get_project(id):
    """
    Get project
    Retreives project with `id`
    ---
    tags:
        - Project
    parameters:
        -   in: path
            name: id
            type: integer
            required: true
            description: Id of the project to retrieve
    responses:
        200:
            description: Project object
        404:
            description: Project not found
    """
    return wrap_response(*projectController.get_project(id=id))

@app.route("/projects", methods=['GET'])
def get_all_projects():
    """
    Get all projects
    Retreives all projects
    ---
    tags:
        - Project
    responses:
        200:
            description: List of projects
    """
    return wrap_response(*projectController.get_all_projects())

@app.route("/project", methods=['DELETE'])
@jwt_required
@body_required
def delete_project():
    """
    Delete project
    Deletes current user's project with the id in request body
    ---
    tags:
        - Project
    parameters:
        -   in: body
            name: id
            type: integer
            required: true
            description: Id of the project to delete
    responses:
        200:
            description: Project deleted successfully
        400:
            description: Failed to delete project
        404:
            description: Current user is not a member of requested project or the project was not found
    """
    if "user_id" in request.get_json():
        return wrap_response(None, "Failed to delete project. Request body must not contain 'user_id'.", 400)

    return wrap_response(*projectController.delete_project(user_id=get_jwt_identity(), **request.get_json()))

# Project Link
@app.route("/project/link", methods=['POST'])
@jwt_required
@body_required
def create_project_link():
    """
    Create project link
    ---
    tags:
        - ProjectLink
    parameters:
        -   in: body
            name: project_id
            type: integer
            required: true
            description: Id of project for which link shall be created
        -   in: body
            name: ProjectLink
            required: true
            description: Project link object containing data to update
            schema:
                $ref: "#/definitions/ProjectLink"
    definitions:
        - schema:
            id: ProjectLink
            properties:
                id:
                    type: integer
                    description: Id of the project link. This property will be assigned a value returned by the database
                name:
                    type: string
                    description: Name of the project link
                url:
                    type: string
                    description: Url of the project link
                project_id:
                    type: integer
                    description: Id of the project
    responses:
        201:
            description: Project link created successfully
        400:
            description: Failed to create project link
    """
    if "user_id" in request.get_json():
        return wrap_response(None, "Failed to create project link. Request body must not contain 'user_id'.", 400)

    return wrap_response(*projectController.create_link(user_id=get_jwt_identity(), **request.get_json()))

@app.route("/project/link", methods=['PUT'])
@jwt_required
@body_required
def update_project_link():
    """
    Update project link
    Updates project link with data in the request body
    ---
    tags:
        - ProjectLink
    parameters:
        -   in: body
            name: project_id
            type: integer
            required: true
            description: Id of the project
        -   in: body
            name: ProjectLink
            required: true
            description: Project link object containing data to update
            schema:
                $ref: "#/definitions/ProjectLink"
    responses:
        200:
            description: Project link updated successfully
        400:
            description: Failed to update project link
        404:
            description: Project link not found
    """
    if "user_id" in request.get_json():
        return wrap_response(None, "Failed to update project link. Request body must not contain 'user_id'.", 400)

    return wrap_response(*projectController.update_link(user_id=get_jwt_identity(), **request.get_json()))

@app.route("/project/link", methods=['DELETE'])
@jwt_required
@body_required
def delete_project_link():
    """
    Delete project link
    Deletes project link with data in the request body
    ---
    tags:
        - ProjectLink
    parameters:
        -   in: body
            name: project_id
            type: integer
            required: true
            description: Id of the project
        -   in: body
            name: link_id
            type: integer
            required: true
            description: Id of the project link to delete
    responses:
        200:
            description: Project link deleted successfully
        400:
            description: Failed to delete project link
        404:
            description: Project link not found
    """
    if "user_id" in request.get_json():
        return wrap_response(None, "Failed to delete project link. Request body must not contain 'user_id'.", 400)

    return wrap_response(*projectController.delete_link(user_id=get_jwt_identity(), **request.get_json()))

# Project Feedback
@app.route("/projects/<project_id>/feedbacks", methods=['POST'])
def create_project_feedback(project_id):
    """
    Create project feedback
    ---
    tags:
        - ProjectFeedback
    parameters:
        -   in: body
            name: ProjectFeedback
            required: true
            description: Project feedback object containing data to update
            schema:
                $ref: "#/definitions/ProjectFeedback"
    definitions:
        - schema:
            id: ProjectFeedback
            properties:
                id:
                    type: integer
                    description: Id of the project feedback. This property will be assigned a value returned by the database
                user_id:
                    type: integer
                    description: Id of the user
                project_id:
                    type: integer
                    description: Id of the project
                rating:
                    type: string
                    description: The rating of the project feedback
                description:
                    type: string
                    description: The body of the project feedback
    responses:
        201:
            description: Project feedback created successfully
        400:
            description: Failed to create project feedback
    """
    if 'project_id' in request.get_json():
        return "Failed to create feedback. Request body can not specify feedback's project_id.", 400

    feedback = projectController.create_feedback(project_id, **request.get_json())

    if feedback == None:
        return "Failed to create feedback.", 400
    else:
        return jsonify(feedback.as_dict()), 201

@app.route("/projects/<project_id>/feedbacks/<feedback_id>", methods=['DELETE'])
def delete_project_feedback(project_id, feedback_id):
    """
    Delete project feedback
    Deletes project feedback with `project_id` and `feedback_id`
    ---
    tags:
        - ProjectFeedback
    parameters:
        -   in: path
            name: project_id
            type: integer
            required: true
            description: Id of the project
        -   in: path
            name: feedback_id
            type: integer
            required: true
            description: Id of the project feedback to delete
    responses:
        200:
            description: Project feedback deleted successfully
        404:
            description: Project feedback not found
    """
    feedback = projectController.delete_feedback(project_id, feedback_id)

    if feedback == None:
        return "", 404
    else:
        return "", 200
