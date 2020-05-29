from tests.conftest import client

def test_create_project(client):
    response = client.get('/projects')
    # assert response.status_code == 405
