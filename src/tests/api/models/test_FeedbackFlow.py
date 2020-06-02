from tests.conftest import client
from tests import User, Project, UserFeedback, ProjectFeedback
from tests.api import create_user_for_test_cases, create_project_for_test_cases

class TestFeedbackFlow(object):

    valid_data_1 = {
        "name": "Foe Joe",
    }

    valid_data_2 = {
        "name": "Jimmy Joe"
    }

    def test_user_to_user_feedback_creation(self, client):
        user1_id = create_user_for_test_cases(self.valid_data_2)
        user2_id = create_user_for_test_cases(self.valid_data_2)
