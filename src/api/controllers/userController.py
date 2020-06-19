from api.models import db, User, UserHasProject, UserLink, UserFeedback
from flask import request, jsonify, session, Flask, redirect, session, url_for
from api import app
from os import environ

session = db.session()

# User
@app.route("/users", methods=['POST'])
def create_user():
    """
    Create user
    ---
    tags:
        - User
    parameters:
        -   in: body
            name: User
            required: true
            description: User object containing data for creation
            schema:
                $ref: "#/definitions/User"
    definitions:
        - schema:
            id: User
            properties:
                id:
                    type: integer
                    description: Id of the user. This property will be assigned a value returned by the database
                name:
                    type: string
                    description: Name of the user
                bio:
                    type: string
                    description: Biography of the user
                languages:
                    type: string
                    description: List of programming languages the user uses
                interests:
                    type: string
                    description: Interests of the user
                location:
                    type: string
                    description: Location of the user
                occupation:
                    type: string
                    description: Formal occupation, eg. student at X or works at Y
                projects:
                    type: array
                    description: List of projects
                    items:
                        $ref: "#/definitions/Project"
                links:
                    type: array
                    description: List of links
                    items:
                        $ref: "#/definitions/UserLink"
                project_feedbacks:
                    type: array
                    description: List of feedbacks given to projects
                    items:
                        $ref: "#/definitions/ProjectFeedback"
                user_feedbacks:
                    type: array
                    description: List of feedbacks given to users
                    items:
                        $ref: "#/definitions/UserFeedback"
                received_feedbacks:
                    type: array
                    description: List of received feedbacks from users
                    items:
                        $ref: "#/definitions/UserFeedback"
    responses:
        201:
            description: User created successfully
        400:
            description: Failed to create user
    """
    try:
        user = User(**request.get_json())
        session.add(user)
        session.commit()

        return jsonify(user.as_dict()), 201
    except:
        session.rollback()
        return "Failed to create user.", 400

@app.route("/users/<id>", methods=['PUT'])
def update_user(id):
    """
    Update user
    Updates user with `id` using the data in request body
    ---
    tags:
        - User
    parameters:
        -   in: path
            name: id
            type: integer
            required: true
            description: Id of user to update
        -   in: body
            name: User
            required: true
            description: User object containing data to update
            schema:
                $ref: "#/definitions/User"
    responses:
        200:
            description: User updated successfully
        400:
            description: Failed to update user
    """
    if 'id' in request.get_json():
        return "Failed to update user. Request body can not specify user's id.", 501

    user = User.query.filter_by(id=id).first()
    if user == None:
        return "Failed to update user.", 400

    for key, value in request.get_json().items():
        if not hasattr(user, key):
            return "Failed to update user.", 400

        for key, value in request.get_json().items():
            setattr(user, key, value)

        db.session.commit()

        return jsonify(user.as_dict()), 200

@app.route("/users/<id>", methods=['GET'])
def get_user(id):
    """
    Get user
    Retreives user with `id`
    ---
    tags:
        - User
    parameters:
        -   in: path
            name: id
            type: integer
            required: true
            description: Id of the user to retrieve
    responses:
        200:
            description: User object
        404:
            description: User not found
    """
    user = User.query.filter_by(id=id).first()

    if user:
        return jsonify(user.as_dict()), 200
    else:
        return "", 404

@app.route("/users", methods=['GET'])
def get_all_users():
    """
    Get all users
    Retreives all users
    ---
    tags:
        - User
    responses:
        200:
            description: List of users
    """
    all_users = User.query.all()

    users = [ user.as_dict() for user in all_users ]

    return jsonify(users), 200

@app.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
    """
    Delete user
    Deletes user with `id`
    ---
    tags:
        - User
    parameters:
        -   in: path
            name: id
            type: integer
            required: true
            description: Id of the user to delete
    responses:
        200:
            description: User deleted successfully
        401:
            description: Not allowed to delete the specified user
        404:
            description: User not found
    """
    if int(current_user.id) == int(id):
        # Remove all user's links
        for link in UserLink.query.filter_by(user_id=id).all():
            db.session.delete(link)

        # Remove user from all projects
        for project in UserHasProject.query.filter_by(user_id=id).all():
            db.session.delete(project)

        user = User.query.filter_by(id=id).first()

        if user == None:
            return "", 404

        db.session.delete(user)
        db.session.commit()

        return "", 200
    else:
        return "You cannot delete an other user", 401

# User Link
@app.route("/users/<user_id>/links", methods=['POST'])
def create_user_link(user_id):
    """
    Create user link
    ---
    tags:
        - UserLink
    parameters:
        -   in: body
            name: UserLink
            required: true
            description: User link object containing data to update
            schema:
                $ref: "#/definitions/UserLink"
    definitions:
        - schema:
            id: UserLink
            properties:
                id:
                    type: integer
                    description: Id of the user link. This property will be assigned a value returned by the database
                name:
                    type: string
                    description: Name of the user link
                url:
                    type: string
                    description: Url of the user link
                user_id:
                    type: integer
                    description: Id of the user
    responses:
        201:
            description: User link created successfully
        400:
            description: Failed to create user link
    """
    if 'user_id' in request.get_json():
        return "Failed to create user link. Request body can not specify link's user_id.", 400

    try:
        link = UserLink(user_id=user_id, **kwargs)
        session.add(link)
        session.commit()

        return jsonify(link.as_dict()), 201
    except:
        session.rollback()
        return "Failed to create user link.", 400

@app.route("/users/<user_id>/links/<link_id>", methods=['PUT'])
def update_user_link(user_id, link_id):
    """
    Update user link
    Updates user link with `user_id` and `link_id` using the data in request body
    ---
    tags:
        - UserLink
    parameters:
        -   in: path
            name: user_id
            type: integer
            required: true
            description: Id of the user
        -   in: path
            name: link_id
            type: integer
            required: true
            description: Id of the user link to update
        -   in: body
            name: UserLink
            required: true
            description: User link object containing data to update
            schema:
                $ref: "#/definitions/UserLink"
    responses:
        200:
            description: User link updated successfully
        400:
            description: Failed to update user link
    """
    if 'user_id' in request.get_json():
        return "Failed to update user link. Request body can not specify link's user_id.", 400
    elif 'link_id' in request.get_json():
        return "Failed to update user link. Request body can not specify link's link_id.", 400

    link = UserLink.query.filter_by(user_id=user_id, id=link_id).first()

    if link == None:
        return "Failed to update user link.", 400

    for key, value in kwargs.items():
        if not hasattr(link, key):
            return "Failed to update user link.", 400

    for key, value in kwargs.items():
        setattr(link, key, value)

    db.session.commit()

    return jsonify(link.as_dict()), 200

@app.route("/users/<user_id>/links", methods=['GET'])
def get_all_user_links(user_id):
    """
    Get all user links
    Retreives all user links with `user_id`
    ---
    tags:
        - UserLink
    parameters:
        -   in: path
            name: user_id
            type: integer
            required: true
            description: Id of the user
    responses:
        200:
            description: List of user links
    """
    all_links = UserLink.query.filter_by(user_id=user_id).all()

    links = [ link.as_dict() for link in all_links ]

    return jsonify(links), 200

@app.route("/users/<user_id>/links/<link_id>", methods=['DELETE'])
def delete_user_link(user_id, link_id):
    """
    Delete user link
    Deletes user link with `user_id` and `link_id`
    ---
    tags:
        - UserLink
    parameters:
        -   in: path
            name: user_id
            type: integer
            required: true
            description: Id of the user
        -   in: path
            name: link_id
            type: integer
            required: true
            description: Id of the user link to delete
    responses:
        200:
            description: User link deleted successfully
        404:
            description: User link not found
    """
    link = UserLink.query.filter_by(user_id=user_id, id=link_id).first()

    if link == None:
        return "", 404

    db.session.delete(link)
    db.session.commit()

    return "", 200

# User Feedback
@app.route("/users/<user_id>/feedbacks", methods=['POST'])
def create_user_feedback(user_id):
    """
    Create user feedback
    ---
    tags:
        - UserFeedback
    parameters:
        -   in: body
            name: UserFeedback
            required: true
            description: User feedback object containing data to update
            schema:
                $ref: "#/definitions/UserFeedback"
    definitions:
        - schema:
            id: UserFeedback
            properties:
                id:
                    type: integer
                    description: Id of the user feedback. This property will be assigned a value returned by the database
                author_id:
                    type: integer
                    description: Id of the author
                user_id:
                    type: integer
                    description: Id of the user
                rating:
                    type: string
                    description: The rating of the user feedback
                description:
                    type: string
                    description: The body of the user feedback
    responses:
        201:
            description: User feedback created successfully
        400:
            description: Failed to create user feedback
    """
    if 'user_id' in request.get_json():
        return "Failed to create feedback. Request body can not specify feedback's user_id.", 400

    try:
        feedback = UserFeedback(user_id=user_id, **request.get_json())
        session.add(feedback)
        session.commit()

        return jsonify(feedback.as_dict()), 201
    except:
        session.rollback()
        return "Failed to create feedback.", 400

@app.route("/users/<user_id>/feedbacks", methods=['GET'])
def get_all_user_feedbacks(user_id):
    """
    Get all user feedbacks
    Retreives all user feedbacks with `user_id`
    ---
    tags:
        - UserFeedback
    parameters:
        -   in: path
            name: user_id
            type: integer
            required: true
            description: Id of the user
    responses:
        200:
            description: List of user feedbacks
    """
    all_feedbacks = UserFeedback.query.filter_by(user_id=user_id).all()

    feedbacks = [ feedback.as_dict() for feedback in all_feedbacks ]

    return jsonify(feedbacks), 200

@app.route("/users/<user_id>/feedbacks/<feedback_id>", methods=['DELETE'])
def delete_user_feedback(user_id, feedback_id):
    """
    Delete user feedback
    Deletes user feedback with `user_id` and `feedback_id`
    ---
    tags:
        - UserFeedback
    parameters:
        -   in: path
            name: user_id
            type: integer
            required: true
            description: Id of the user
        -   in: path
            name: feedback_id
            type: integer
            required: true
            description: Id of the user feedback to delete
    responses:
        200:
            description: User feedback deleted successfully
        404:
            description: User feedback not found
    """
    feedback = UserFeedback.query.filter_by(user_id=user_id, id=feedback_id).first()

    if feedback == None:
        return "", 404

    db.session.delete(feedback)
    db.session.commit()

    return "", 200
