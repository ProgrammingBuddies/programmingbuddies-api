from tests.conftest import client
from tests import db, User, UserLink, UserFeedback
from tests.api import create_user_for_test_cases, create_user_link_for_test_cases, create_user_feedback_for_test_cases
from tests.api import delete_user_for_test_cases, create_access_token_for_test_cases

class TestUserView(object):

    # valid data for user creation
    valid_data = {
        'name': 'L Jone',
        'bio': 'coding...',
        'languages': 'FR',
        'interests': 'Nothing',
        'location': 'X',
        'occupation': 'cashier'
    }


    def test_update_user(self, client):
        token, _ = create_access_token_for_test_cases(self.valid_data)

        #for now we will allow empty body.
        response = client.put('/user', headers={"Authorization": f"Bearer {token}"}, json={})
        assert response.status_code == 200

        response = client.put('/user', headers={"Authorization": f"Bearer {token}"}, json={"name": "Updated Name"})
        assert response.status_code == 200

        assert response.get_json()['data']['name'] == "Updated Name"

    def test_delete_user(self, client):
        token, _ = create_access_token_for_test_cases(self.valid_data)

        response = client.delete('/user', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200

        response = client.delete('/user', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 404
        

    def test_get_user(self, client):
        token, user = create_access_token_for_test_cases(self.valid_data)
        
        response = client.get('/user', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.get_json() == {"data": user.as_dict(), "msg": "OK"}

        delete_user_for_test_cases(user)
        
        response = client.get('/user', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 404


        

    def test_get_all_users(self, client):
        create_user_for_test_cases(self.valid_data)

        self.valid_data = {
            'name': 'Valid',
            'bio': 'new',
            'languages': 'DE',
            'interests': 'e',
            'location': 'nowhere',
            'occupation': 'cashier2.1'
        }

        create_user_for_test_cases(self.valid_data)

        response = client.get('/users')
        assert response.status_code == 200

        users_list = User.query.all()
        users_dict = [users_list[0].as_dict(), users_list[1].as_dict()]
        assert response.get_json() == [users_list[0].as_dict(), users_list[1].as_dict()]

        db.session.delete(users_list[0])
        db.session.commit()

        response = client.get('/users')
        assert response.status_code == 200
        assert response.get_json() == [users_dict[1]]

    def test_create_user_link(self, client):
        token, user = create_access_token_for_test_cases(self.valid_data)
        url = '/user/link'

        response = client.post(url, headers={"Authorization": f"Bearer {token}"}, json={"id": 23})
        assert response.status_code == 400

        response = client.post(url, headers={"Authorization": f"Bearer {token}"}, json={"name": "Smedia", "url": "http://s.media"})
        assert response.status_code == 201

        response = client.post(url, headers={"Authorization": f"Bearer {token}"}, json={"name": None, "url": "http://l.co"})
        assert response.status_code == 400

        response = client.post(url, headers={"Authorization": f"Bearer {token}"}, json={"name": "WORK"})
        assert response.status_code == 400

    def test_update_user_link(self, client):
        token, user = create_access_token_for_test_cases(self.valid_data)
        link = create_user_link_for_test_cases({"name": "Discord", "url": "http://dc.com/my", "user_id": user.id})

        url = "/user/link"

        response = client.put(url, headers={"Authorization": f"Bearer {token}"}, json={"name": "Portfolio"})
        assert response.status_code == 400


        response = client.put(url, headers={"Authorization": f"Bearer {token}"}, json={"id": link['id'], "nonsense": "value"})
        assert response.status_code == 400

        response = client.put(url, headers={"Authorization": f"Bearer {token}"}, json={"id": 1337, "name": "burt"})
        assert response.status_code == 404

        # notice: Should we respond to update_user request without json data with status code 200?
        # response = client.post(url, json={})
        # assert response.status_code == 400

        response = client.put(url, headers={"Authorization": f"Bearer {token}"}, json={"id": link['id'], "name": "New Name"})
        assert response.status_code == 200
        assert response.get_json()["data"]["name"] == "New Name"

    def test_get_all_user_links(self, client):
        token, user = create_access_token_for_test_cases(self.valid_data)
        link1 = create_user_link_for_test_cases({"name": "Discord", "url": "http://dc.com/my", "user_id": user.id})
        link2 = create_user_link_for_test_cases({"name": "PB", "url": "http://pb.com/ur234", "user_id": user.id})

        response = client.get("/user/links", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.get_json() == {"data": [link1, link2], "msg": "OK"}

    def test_delete_user_link(self, client):
        token, user = create_access_token_for_test_cases(self.valid_data)
        link1 = create_user_link_for_test_cases({"name": "Discord", "url": "http://dc.com/my", "user_id": user.id})
        link2 = create_user_link_for_test_cases({"name": "PB", "url": "http://pb.com/ur234", "user_id": user.id})

        response = client.delete("/user/link", headers={"Authorization": f"Bearer {token}"}, json={"id": 1337})
        assert response.status_code == 404

        response = client.delete("/user/link", headers={"Authorization": f"Bearer {token}"}, json={"id": link1["id"]})
        assert response.status_code == 200

        recorded_links = UserLink.query.all()
        assert len(recorded_links) == 1
        assert link1 not in recorded_links

    def test_create_user_feedback(self, client):
        user1 = create_user_for_test_cases(self.valid_data)

        self.valid_data["name"] = "Other name"
        user2 = create_user_for_test_cases(self.valid_data)

        url = '/users/{}/feedbacks'.format(user2["id"])
        response = client.post(url, json={"user_id": user2["id"]})
        assert response.status_code == 400

        feedback = {
            "author_id": int(user1["id"]),
            "rating": 5,
            "description": "Cool guy!",
        }

        response = client.post(url, json=feedback)
        assert response.status_code == 201

    def test_get_all_user_feedbacks(self, client):
        token1, user1 = create_access_token_for_test_cases(self.valid_data)

        self.valid_data["name"] = "new user2"
        token2, user2 = create_access_token_for_test_cases(self.valid_data)

        self.valid_data["name"] = "new user3"
        token3, user3 = create_access_token_for_test_cases(self.valid_data)

        create_user_feedback_for_test_cases(user1.as_dict(), user2.as_dict())
        create_user_feedback_for_test_cases(user3.as_dict(), user1.as_dict())
        create_user_feedback_for_test_cases(user2.as_dict(), user1.as_dict())

        url = "/user/feedbacks"

        response = client.get(url, json={"id": user1.id})
        r_json = response.get_json()['data']
        assert len(r_json) == 2
        assert [r_json[0]["user_id"], r_json[0]["author_id"], r_json[1]["user_id"], r_json[1]["author_id"]] == \
               [user1.id, user3.id, user1.id, user2.id]

        response = client.get(url, json={"id": user2.id})
        r_json = response.get_json()['data']
        assert len(r_json) == 1
        assert [r_json[0]["user_id"], r_json[0]["author_id"]] == [user2.id, user1.id]

    def test_delete_user_feedback(self, client):
        user1 = create_user_for_test_cases(self.valid_data)

        self.valid_data["name"] = "delete user2"
        user2 = create_user_for_test_cases(self.valid_data)

        fb1 = create_user_feedback_for_test_cases(user1, user2)
        fb2 = create_user_feedback_for_test_cases(user1, user2)

        url = "/users/{0}/feedbacks/{1}"

        response = client.delete(url.format(user1["id"], 0))
        assert response.status_code == 404

        response = client.delete(url.format(0, fb1["id"]))
        assert response.status_code == 404

        response = client.delete(url.format(user2["id"], fb1["id"]))
        assert response.status_code == 200
        assert UserFeedback.query.filter_by(user_id=user2["id"]).count() == 1
