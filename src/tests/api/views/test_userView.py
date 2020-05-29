from tests.conftest import client
from tests import db, User

class TestUserView(object):

    valid_data = {
        'name': 'L Jone',
        'bio': 'coding...',
        'languages': 'FR',
        'interests': 'Nothing',
        'location': 'X',
        'occupation': 'cashier'
    }

    def create_user_for_test_cases(self):
        new_user = User(**self.valid_data)
        db.session.add(new_user)
        db.session.commit()
        return new_user.id

    def test_create_user(self, client):
        response = client.post('/users', json=self.valid_data)
        assert response.status_code == 201

        response = client.post('/users', json={})
        assert response.status_code == 400

    def test_update_user(self, client):
        user_id = self.create_user_for_test_cases()

        response = client.post('/users/1', json={})
        assert response.status_code == 400

        # notice: Should we respond to update_user request without json data with status code 200?
        response = client.post('/users/{}'.format(user_id), json={})
        assert response.status_code == 400

        response = client.post('/users/{}'.format(user_id), json={"name": "Updated Name"})
        assert response.status_code == 200

        # created_user = User.query.filter_by(id=user_id).first()
        assert response.get_json()['name'] == "Updated Name"

    def test_delete_user(self, client):
        user_id = None
        response = client.delete('/users/{}'.format(user_id))
        assert response.status_code == 404

        user_id = self.create_user_for_test_cases()
        response = client.delete('/users/{}'.format(user_id))
        assert response.status_code == 200

    def test_get_user(self, client):
        user_id = None
        response = client.get('/users/{}'.format(user_id))
        assert response.status_code == 404

        user_id = self.create_user_for_test_cases()
        response = client.get('/users/{}'.format(user_id))
        assert response.status_code == 200

        created_user = User.query.filter_by(id=user_id).first()
        assert response.get_json() == created_user.as_dict()
