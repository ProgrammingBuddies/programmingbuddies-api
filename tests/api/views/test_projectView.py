from tests.conftest import client
from tests import db, Project, ProjectLink
from tests.api import create_project_for_test_cases, create_project_link_for_test_cases, create_access_token_for_test_cases, user_join_project_for_test_cases

class TestProjectView(object):

    # valid data for user creation
    valid_user_data = {
        'name': 'L Jone',
        'bio': 'coding...',
        'languages': 'FR',
        'interests': 'Nothing',
        'location': 'X',
        'occupation': 'cashier'
    }

    valid_project_data = {
        'name': 'PB api',
        'description': 'A cool project',
        'development_status': 1,
        'repository': 'http://github.xy.com'
    }

    def test_create_project(self, client):
        token, _ = create_access_token_for_test_cases(self.valid_user_data)

        response = client.post('/project', headers={"Authorization": f"Bearer {token}"}, json={"name": "Project"})
        assert response.status_code == 400

        response = client.post('/project', headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 400

        response = client.post('/project')
        assert response.status_code == 401

        response = client.post('/project', headers={"Authorization": f"Bearer {token}"}, json=self.valid_project_data)
        assert response.status_code == 201

    def test_update_project(self, client):
        token, _ = create_access_token_for_test_cases(self.valid_user_data)

        # project id doesn't exist
        response = client.put('/project', headers={"Authorization": f"Bearer {token}"}, json={'id': 0, 'name': 'Updated PB'})
        assert response.status_code == 404

        project = create_project_for_test_cases(self.valid_project_data)
        project_id = project["id"]

        response = client.put('/project', headers={"Authorization": f"Bearer {token}"}, json={'id': project_id, 'description': 'updated desc'})
        project = Project.query.filter_by(id=project_id).first()
        assert project.description == 'updated desc'

    def test_delete_project(self, client):
        token, user = create_access_token_for_test_cases(self.valid_user_data)

        response = client.delete('/project/{}'.format(0), headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 404

        project1 = create_project_for_test_cases(self.valid_project_data)
        user_join_project_for_test_cases(user, project1)

        self.valid_project_data["name"] = "p2 name"
        project2 = create_project_for_test_cases(self.valid_project_data)
        user_join_project_for_test_cases(user, project2)

        response = client.delete('/project/{}'.format(project1["id"]), headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200

    def test_get_project(self, client):
        response = client.get('/project/{}'.format(0))
        assert response.status_code == 404

        project = create_project_for_test_cases(self.valid_project_data)
        response = client.get('/project/{}'.format(project["id"]))
        assert response.status_code == 200
        assert response.get_json()["data"]["name"] == project["name"]

    def test_get_all_projects(self, client):
        project1 = create_project_for_test_cases(self.valid_project_data)

        self.valid_project_data["name"] = "allproject2"
        project2 = create_project_for_test_cases(self.valid_project_data)
        response = client.get('/project/all')

        assert response.status_code == 200
        r = response.get_json()
        assert [r["data"][0]["name"], r["data"][1]["name"]] == [project1["name"], project2["name"]]

    def test_create_project_link(self, client):
        token, _ = create_access_token_for_test_cases(self.valid_user_data)

        project = create_project_for_test_cases(self.valid_project_data)
        url = '/project/link'

        response = client.post(url, headers={"Authorization": f"Bearer {token}"}, json={"user_id": 0})
        assert response.status_code == 400

        response = client.post(url, headers={"Authorization": f"Bearer {token}"}, json={"project_id": project["id"], "name": "Main link", "url": "http://main.link"})
        assert response.status_code == 201

    def test_update_project_link(self, client):
        token, _ = create_access_token_for_test_cases(self.valid_user_data)

        p1 = create_project_for_test_cases(self.valid_project_data)
        p1_link = create_project_link_for_test_cases(
            {
            "name": "Plink",
            "url": "https://xll.com",
            "project_id": p1["id"]
        })

        url = '/project/link'

        response = client.put(url, headers={"Authorization": f"Bearer {token}"}, json={"project_id": p1["id"], "id": 0})
        assert response.status_code == 404

        response = client.put(url, headers={"Authorization": f"Bearer {token}"}, json={"project_id": 0, "id": p1_link["id"]})
        assert response.status_code == 404

        response = client.put(url, headers={"Authorization": f"Bearer {token}"}, json={"project_id": p1["id"], "id": p1_link["id"], "name": "Nlink"})
        assert response.status_code == 200
        assert response.get_json()["data"]["name"] == "Nlink"

    def test_delete_project_link(self, client):
        token, _ = create_access_token_for_test_cases(self.valid_user_data)

        url = '/project/link'

        response = client.delete(url, headers={"Authorization": f"Bearer {token}"}, json={"project_id": 0, "id": 0})
        assert response.status_code == 404

        p1 = create_project_for_test_cases(self.valid_project_data)
        p_link1 = create_project_link_for_test_cases(
            {
            "name": "Plink",
            "url": "https://xll.com",
            "project_id": p1["id"]
        })
        p_link2 = create_project_link_for_test_cases(
            {
            "name": "Other",
            "url": "https://pp.com",
            "project_id": p1["id"]
        })


        response = client.delete(url, headers={"Authorization": f"Bearer {token}"}, json={"project_id": p1["id"], "id": p_link1["id"]})
        assert response.status_code == 200
        items = ProjectLink.query.all()
        assert len(items) == 1
        assert items[0].name == "Other"
