from flask_inputs import Inputs
from wtforms.validators import InputRequired
from wtforms.validators import URL


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
