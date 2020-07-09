from flask_inputs import Inputs
from wtforms.validators import InputRequired, URL, Length


class UserLinkCreateValidation(Inputs):
    json = {
        'name': [InputRequired("name required")],
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
