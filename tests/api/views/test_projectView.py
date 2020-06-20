from tests.conftest import client
from tests import db, Project, ProjectLink
from tests.api import create_project_for_test_cases, create_project_link_for_test_cases

class TestProjectView(object):

    valid_data = {
        'name': 'PB api',
        'description': 'A cool project',
        'repository': 'http://github.xy.com'
    }

    def test_create_project(self, client):
        response = client.post('/projects', json={"name": "Project"})
        assert response.status_code == 400

        response = client.post('/projects', json=self.valid_data)
        assert response.status_code == 201

        # response = client.post('/projects')
        # assert response.status_code == 400

    def test_update_project(self, client):

        # project id doesn't exist
        response = client.post('/projects/0', json={'name': 'Updated PB'})

        # notice: should return 404 when doesen't exist insted of 400
        assert response.status_code == 404

        project_id = create_project_for_test_cases(self.valid_data)
        response = client.post('/projects/{}'.format(project_id), json={'description': 'updated desc'})
        project = Project.query.filter_by(id=project_id).first()
        assert project.description == 'updated desc'

    def test_delete_project(self, client):
        response = client.delete('/projects/0')
        assert response.status_code == 404

        project1 = create_project_for_test_cases(self.valid_data)

        self.valid_data["name"] = "p2 name"
        project2 = create_project_for_test_cases(self.valid_data)

        response = client.delete('/projects/{}'.format(project1["id"]))
        assert response.status_code == 204

    def test_get_project(self, client):
        response = client.get('/projects/{}'.format(0))
        assert response.status_code == 404

        project = create_project_for_test_cases(self.valid_data)
        response = client.get('/projects/{}'.format(project["id"]))
        assert response.status_code == 200
        assert response.get_json()["name"] == project["name"]

    def test_get_all_projects(self, client):
        project1 = create_project_for_test_cases(self.valid_data)

        self.valid_data["name"] = "allproject2"
        project2 = create_project_for_test_cases(self.valid_data)
        response = client.get('/projects')

        assert response.status_code == 200
        r = response.get_json()
        assert [r[0]["name"], r[1]["name"]] == [project1["name"], project2["name"]]

    def test_create_project_link(self, client):
        project = create_project_for_test_cases(self.valid_data)
        url = '/projects/{}/links'.format(project["id"])

        response = client.post(url, json={"user_id": 0})
        assert response.status_code == 400

        response = client.post(url, json={"name": "Main link", "url": "http://main.link"})
        assert response.status_code == 201

    def test_update_project_link(self, client):
        p1 = create_project_for_test_cases(self.valid_data)
        p1_link = create_project_link_for_test_cases(
            {
            "name": "Plink",
            "url": "https://xll.com",
            "project_id": p1["id"]
        })

        url = '/projects/{0}/links/{1}'

        # notice: this shouldn't give 500 error
        # response = client.post(url.format(p1["id"], 0))
        # assert response.status_code == 404

        # notice: this shouldn't give 500 error
        # response = client.post(url.format(0, p1_link["id"]))
        # assert response.status_code == 404

        response = client.post(url.format(p1["id"], p1_link["id"]), json={"name": "Nlink"})
        assert response.status_code == 200
        assert response.get_json()["name"] == "Nlink"

    def test_get_all_project_links(self, client):
        p1 = create_project_for_test_cases(self.valid_data)
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

        response = client.get('/projects/{}/links'.format(p1["id"]))
        assert response.status_code == 200
        assert response.get_json() == [p_link1, p_link2]

    def test_delete_project_link(self, client):
        url = '/projects/{0}/links/{1}'

        response = client.delete(url.format(0, 0))
        assert response.status_code == 404

        p1 = create_project_for_test_cases(self.valid_data)
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


        response = client.delete(url.format(p1["id"], p_link1["id"]))
        assert response.status_code == 204
        items = ProjectLink.query.all()
        assert len(items) == 1
        assert items[0].name == "Other"
