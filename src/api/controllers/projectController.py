from api.models import db, Project, UserHasProject, ProjectLink, ProjectFeedback
from flask import request, jsonify
from api import app

session = db.session()

@app.route("/projects", methods=['POST'])
def create_project():
    """
    Create project
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
                    description: List of programming languages the project uses
                development_status:
                    type: integer
                    description: Development status of the project
                creation_date:
                    type: string
                    description: Creation date of the project
                release_date:
                    type: string
                    description: Release date of the project
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
    """
    try:
        project = Project(**request.get_json())
        session.add(project)
        session.commit()

        return jsonify(project.as_dict()), 201
    except:
        session.rollback()
        return "Failed to create project.", 400

@app.route("/projects/<id>", methods=['PUT'])
def update_project(id):
    """
    Update project
    Updates project with `id` using the data in request body
    ---
    tags:
        - Project
    parameters:
        -   in: path
            name: id
            type: integer
            required: true
            description: Id of project to update
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
            description: Project not found
    """
    if 'id' in request.get_json():
        return "Failed to update project. Request body can not specify project's id.", 501

    project = Project.query.filter_by(id=id).first()

    if project == None:
        return "", 404

    for key, value in request.get_json().items():
        if not hasattr(project, key):
            return "Failed to update project.", 400

    for key, value in request.get_json().items():
        setattr(project, key, value)

    db.session.commit()

    return jsonify(project.as_dict()), 200

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
    project = Project.query.filter_by(id=id).first()

    if project:
        return jsonify(project.as_dict()), 200
    else:
        return "", 404

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
    all_projects = Project.query.all()

    projects = [ project.as_dict() for project in all_projects ]

    return jsonify(projects), 200

@app.route("/projects/<id>", methods=['DELETE'])
def delete_project(id):
    """
    Delete project
    Deletes project with `id`
    ---
    tags:
        - Project
    parameters:
        -   in: path
            name: id
            type: integer
            required: true
            description: Id of the project to delete
    responses:
        204:
            description: Project deleted successfully
        404:
            description: Project not found
    """
    # Remove all project's links
    for link in ProjectLink.query.filter_by(project_id=id).all():
        db.session.delete(link)

    # Remove project from all users
    for project in UserHasProject.query.filter_by(project_id=id).all():
        db.session.delete(project)

    project = Project.query.filter_by(id=id).first()

    if project == None:
        return "", 404

    db.session.delete(project)
    db.session.commit()

    return "", 204

# Project Link
@app.route("/projects/<project_id>/links", methods=['POST'])
def create_project_link(project_id):
    """
    Create project link
    ---
    tags:
        - ProjectLink
    parameters:
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
    if 'project_id' in request.get_json():
        return "Failed to create project link. Request body can not specify link's project_id.", 400

    try:
        link = ProjectLink(project_id=project_id, **request.get_json())
        session.add(link)
        session.commit()

        return jsonify(link.as_dict()), 201
    except:
        session.rollback()
        return "Failed to create project link.", 400

@app.route("/projects/<project_id>/links/<link_id>", methods=['PUT'])
def update_project_link(project_id, link_id):
    """
    Update project link
    Updates project link with `project_id` and `link_id` using the data in request body
    ---
    tags:
        - ProjectLink
    parameters:
        -   in: path
            name: project_id
            type: integer
            required: true
            description: Id of the project
        -   in: path
            name: link_id
            type: integer
            required: true
            description: Id of the project link to update
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
        404
            description: Project link not found
    """
    if 'project_id' in request.get_json():
        return "Failed to update project link. Request body can not specify link's project_id.", 400
    elif 'link_id' in request.get_json():
        return "Failed to update project link. Request body can not specify link's link_id.", 400

    link = ProjectLink.query.filter_by(project_id=project_id, id=link_id).first()

    if link == None:
        return "", 404

    for key, value in request.get_json().items():
        if not hasattr(link, key):
            return "Failed to update project link.", 400

    for key, value in request.get_json().items():
        setattr(link, key, value)

    db.session.commit()

    return jsonify(link.as_dict()), 200

@app.route("/projects/<project_id>/links", methods=['GET'])
def get_all_project_links(project_id):
    """
    Get all project links
    Retreives all project links with `project_id`
    ---
    tags:
        - ProjectLink
    parameters:
        -   in: path
            name: project_id
            type: integer
            required: true
            description: Id of the project
    responses:
        200:
            description: List of project links
    """
    all_links = ProjectLink.query.filter_by(project_id=project_id).all()

    links = [ link.as_dict() for link in all_links ]

    return jsonify(links), 200

@app.route("/projects/<project_id>/links/<link_id>", methods=['DELETE'])
def delete_project_link(project_id, link_id):
    """
    Delete project link
    Deletes project link with `project_id` and `link_id`
    ---
    tags:
        - ProjectLink
    parameters:
        -   in: path
            name: project_id
            type: integer
            required: true
            description: Id of the project
        -   in: path
            name: link_id
            type: integer
            required: true
            description: Id of the project link to delete
    responses:
        204:
            description: Project link deleted successfully
        404:
            description: Project link not found
    """
    link = ProjectLink.query.filter_by(project_id=project_id, id=link_id).first()

    if link == None:
        return "", 404

    db.session.delete(link)
    db.session.commit()

    return "", 204

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

    try:
        feedback = ProjectFeedback(project_id=project_id, **request.get_json())
        session.add(feedback)
        session.commit()

        return jsonify(feedback.as_dict()), 201
    except:
        session.rollback()
        return "Failed to create feedback.", 400

@app.route("/projects/<project_id>/feedbacks", methods=['GET'])
def get_all_project_feedbacks(project_id):
    """
    Get all project feedbacks
    Retreives all project feedbacks with `project_id`
    ---
    tags:
        - ProjectFeedback
    parameters:
        -   in: path
            name: project_id
            type: integer
            required: true
            description: Id of the project
    responses:
        200:
            description: List of project feedbacks
    """
    all_feedbacks = ProjectFeedback.query.filter_by(project_id=project_id).all()

    feedbacks = [ feedback.as_dict() for feedback in all_feedbacks ]

    return jsonify(feedbacks), 200

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
        204:
            description: Project feedback deleted successfully
        404:
            description: Project feedback not found
    """
    feedback = ProjectFeedback.query.filter_by(project_id=project_id, id=feedback_id).first()

    if feedback == None:
        return "", 404

    db.session.delete(feedback)
    db.session.commit()

    return "", 204
