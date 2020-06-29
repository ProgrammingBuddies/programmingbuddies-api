from flask import request, jsonify, session, Flask, redirect, session, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from api import app
from api.utils import wrap_response, body_required
from api.controllers import userController
from os import environ

# User
@app.route("/user", methods=['PUT'])
@jwt_required
@body_required
def update_user():
    """
    Update user
    Updates authenticated user with the data in request body
    ---
    tags:
        - User
    parameters:
        -   in: body
            name: User
            required: true
            description: User attributes to update. Any combination of attributes is valid
            schema:
                id: UserUpdate
                properties:
                    name:
                        type: string
                        description: (Optional) Name of the user
                    bio:
                        type: string
                        description: (Optional) Biography of the user
                    languages:
                        type: string
                        description: (Optional) List of programming languages the user uses
                    interests:
                        type: string
                        description: (Optional) Interests of the user
                    location:
                        type: string
                        description: (Optional) Location of the user
                    occupation:
                        type: string
                        description: (Optional) Formal occupation, eg. student at X or works at Y
    responses:
        200:
            description: User updated successfully
        400:
            description: Bad Request. Forbidden Parameters used
        404:
            description: User the token belonged to doesn't exist anymore
    """

    if 'id' in request.get_json():
        return wrap_response(None, "Failed to update user. Request body can not specify user's id.", 400)

    return wrap_response(*userController.update_user(get_jwt_identity(), **request.get_json()))

@app.route("/user", methods=['GET'])
@jwt_required
def get_user():
    """
    Get user
    Retreives authenticated user
    ---
    tags:
        - User
    responses:
        200:
            description: User object
        404:
            description: User the token belonged to doesn't exist anymore
    """
    return wrap_response(*userController.get_user_from_jwt())

@app.route("/user", methods=['DELETE'])
@jwt_required
def delete_user():
    """
    Delete user
    Deletes authenticated user
    ---
    tags:
        - User
    responses:
        200:
            description: User deleted successfully
        404:
            description: User the token belonged to doesn't exist anymore
    """

    return wrap_response(*userController.delete_user(get_jwt_identity()))

# User Link
@app.route("/user/link", methods=['POST'])
@jwt_required
@body_required
def create_user_link():
    """
    Create a link for the authenticated user
    ---
    tags:
        - UserLink
    parameters:
        -   in: body
            name: UserLink
            required: true
            description: User link object
            schema:
                id: UserLinkCreate
                properties:
                    name:
                        type: string
                        description: Name of the user link
                    url:
                        type: string
                        description: Url of the user link
    responses:
        201:
            description: User link created successfully
        400:
            description: Failed to create user link
        404:
            description: User doesnt Exist.
    """

    return wrap_response(*userController.create_link(get_jwt_identity(), **request.get_json()))

@app.route("/user/link", methods=['PUT'])
@jwt_required
@body_required
def update_user_link():
    """
    Update user link
    Updates one of the authenticated user's links as specified by the link_id
    ---
    tags:
        - UserLink
    parameters:
        -   in: body
            name: UserLink
            required: true
            description: User link object containing data to update
            schema:
                id: UserLinkUpdate
                properties:
                    id:
                        type: integer
                        description: Id of the user link. This property will be assigned a value returned by the database
                    name:
                        type: string
                        description: (optional) Name of the user link
                    url:
                        type: string
                        description: (optional)Url of the user link
    responses:
        200:
            description: User link updated successfully
        400:
            description: Failed to update user link
        404:
            description: User or link don't exist
    """

    return wrap_response(*userController.update_link(get_jwt_identity(), **request.get_json()))

@app.route("/user/links", methods=['GET'])
@jwt_required
def get_all_user_links():
    """
    Get all user links
    Retreives all links of the authenticated user
    ---
    tags:
        - UserLink
    responses:
        200:
            description: List of user links
        404:
            description: User not found
    """
    all_links, msg, code = userController.get_all_links(get_jwt_identity())
    links = [link for link in all_links]
    return wrap_response(links, msg, code)

@app.route("/user/link", methods=['DELETE'])
@jwt_required
@body_required
def delete_user_link():
    """
    Delete user link
    Deletes one of the authenticated user's links as specified by the link_id
    ---
    tags:
        - UserLink
    parameters:
        -   in: body
            name: UserLink
            required: true
            description: User link object containing data to update
            schema:
                id: UserLinkdelete
                properties:
                    id:
                        type: integer
                        description: Id of the user link. This property will be assigned a value returned by the database
    responses:
        200:
            description: User link deleted successfully
        404:
            description: User link not found
    """
    return wrap_response(*userController.delete_link(get_jwt_identity(), **request.get_json()))

# User Feedback
@app.route("/user/feedback", methods=['POST'])
@jwt_required
@body_required
def create_user_feedback():
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
                properties:
                    id:
                        description: Id of the user this feedback is meant for
                    rating:
                        description: Rating of the feedback
                    description:
                        description: Comment of the feedback
    responses:
        201:
            description: User feedback created successfully
        400:
            description: Failed to create user feedback
    """

    return wrap_response(*userController.create_feedback(get_jwt_identity(), **request.get_json()))

@app.route("/user/feedbacks", methods=['GET'])
@body_required
def get_all_user_feedbacks():
    """
    Get all user feedbacks
    Retreives all of the specified user's feedbacks
    ---
    parameters:
        -   in: body
            name: UserFeedbackGet
            required: true
            description: User feedback object containing data to update
            schema:
                properties:
                    id:
                        type: integer
                        description: id of the user
    tags:
        - UserFeedback
    responses:
        200:
            description: List of user feedbacks
    """
    all_feedbacks, msg, code = userController.get_all_feedbacks(**request.get_json())

    feedbacks = [ feedback for feedback in all_feedbacks ]

    return wrap_response(feedbacks, msg, code)

@app.route("/user/feedback", methods=['DELETE'])
@jwt_required
@body_required
def delete_user_feedback():
    """
    Delete user feedback
    Deletes user feedback with `user_id` and `feedback_id`
    ---
    tags:
        - UserFeedback
    parameters:
        -   in: body
            name: UserFeedbackGet
            required: true
            description: User feedback object containing data to update
            schema:
                properties:
                    id:
                        type: integer
                        description: id of the user
    responses:
        200:
            description: User feedback deleted successfully
        404:
            description: User feedback not found
    """
    return wrap_response(*userController.delete_feedback(get_jwt_identity(), **request.get_json()))
