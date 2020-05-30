from tests.conftest import client
from tests import db, Project
from datetime import datetime

class TestPorjectView(object):

    valid_data = {
        'name': 'PB api',
        'description': 'A cool project',
        'repository': 'http://github.xy.com'
    }

    def create_project_for_test_cases(self):
        new_project = Project(**self.valid_data)
        db.session.add(new_project)
        db.session.commit()
        return new_project.id

    def test_create_project(self, client):
        response = client.post('/projects', json={"name": "Project"})
        assert response.status_code == 400

        response = client.post('/projects', json=self.valid_data)
        assert response.status_code == 201

        # response = client.post('/projects')
        # assert response.status_code == 400

    def test_update_project(self, client):

        # project id doesn't exist
        response = client.post('/projects/no_id', json={'name': 'Updated PB'})
        assert response.status_code == 404

        project_id = self.create_project_for_test_cases()
        response = client.post('/projects/{}'.format(project_id), json={'description': 'updated desc'})
        project = Project.query.filter_by(id=project_id).first()
        assert project.description == 'updated desc'
