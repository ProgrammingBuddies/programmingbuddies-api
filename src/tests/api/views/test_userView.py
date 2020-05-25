from tests import client

def test_create_user(client):
    send_data = {
        'name': 'L Jone',
        'bio': 'coding...',
        'languages': 'FR',
        'interests': 'Nothing',
        'location': 'X',
        'occupation': 'cashier'
    }

    response = client.post('/users', json=send_data)
    assert response.status_code == 201
    # assert response.get_json() ==
