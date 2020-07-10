from flask_inputs import Inputs
from wtforms.validators import InputRequired, URL, Length


class UserLinkCreateValidation(Inputs):
    json = {
        'name': [InputRequired("name required"), Length(max=80, message="name too big")],
        'url': [InputRequired("url required"), URL()]
    }


class UserLinkUpdateValidation(Inputs):
    json = {
        'id': [InputRequired("id required")],
        'url': [URL()]
    }


class UserFeedbackCreateValidation(Inputs):
    json = {
        'user_id': [InputRequired("user_id required")],
        'rating': [InputRequired("rating required")],
        'description': [Length(max=255, message="description too big")]
    }


class UserUpdateValidation(Inputs):
    json = {
        'id': [InputRequired("id required")],
        'name': [Length(max=80, message="name too big")],
        'location': [Length(max=80, message="name too big")],
        'occupation': [Length(max=80, message="name too big")]
    }

class UserGetValidation(Inputs):
    json = {
        'name': [Length(max=80, message="name too big")],
        'location': [Length(max=80, message="name too big")],
        'occupation': [Length(max=80, message="name too big")]
    }
