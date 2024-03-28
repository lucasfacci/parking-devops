import pytest
from src import create_app


class TestApplication():

    @pytest.fixture
    def client(self):
        app = create_app('config.MockConfig')
        return app.test_client()

    @pytest.fixture
    def valid_parking(self):
        return {
            'plate': 'GDF8F62',
            'brand': 'volkswagen',
            'model': 'gol',
            'color': 'black',
            'status': 'parked'
        }

    @pytest.fixture
    def invalid_parking(self):
        return {
            'brand': 'volkswagen',
            'model': 'gol',
            'color': 'black',
            'status': 'parked'
        }

    @pytest.fixture
    def sample_parking_uuid(self, client, valid_parking):
        response = client.post('/parking', json=valid_parking)
        return response.json['uuid']

    def test_get_parkings(self, client):
        response = client.get('/parkings')
        assert response.status_code == 200

    def test_get_parking(self, client, sample_parking_uuid):
        response = client.get(f'/parking/{sample_parking_uuid}')
        assert response.status_code == 200
        assert response.json[0]['plate'] == 'GDF8F62'
        assert response.json[0]['brand'] == 'volkswagen'
        assert response.json[0]['model'] == 'gol'
        assert response.json[0]['color'] == 'black'
        assert response.json[0]['status'] == 'parked'
        assert response.json[0]['entry'] is not None
        assert response.json[0].get('exit') is None
        assert response.json[0]['total_amount'] == 5.0

        response = client.get('/parking/00000000-0000-0000-0000-000000000000')
        assert response.status_code == 404
        assert b'Parking not found.' in response.data

    def test_post_parking(self, client, valid_parking, invalid_parking):
        # Testing valid parking
        response = client.post('/parking', json=valid_parking)
        assert response.status_code == 200
        assert response.json['plate'] == 'GDF8F62'
        assert response.json['entry'] is not None
        assert response.json['total_amount'] is not None

        # Testing invalid parking
        response = client.post('/parking', json=invalid_parking)
        assert response.status_code == 400
        assert b'This field cannot be blank.' in response.data
