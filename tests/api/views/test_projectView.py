from tests.conftest import client
from tests import db, Project

from tests.api import create_project_for_test_cases
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

        # project_id = self.create_project_for_test_cases()
        # response = client.delete('/project/{}'.format(project_id))
        # assert response.status_code == 202

    def test_create_porject_link(self, client):
        project = create_project_for_test_cases(self.valid_data)
        url = '/projects/{}/links'.format(project["id"])

        response = client.post(url, json={"user_id": 0})
        assert response.status_code == 400

        response = client.post(url, json={"name": "Main link", "url": "http://main.link"})
        assert response.status_code == 201
