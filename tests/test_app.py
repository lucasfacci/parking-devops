import pytest
from src import create_app


class TestApplication():

    @pytest.fixture
    def client(self):
        app = create_app('config.MockConfig')
        return app.test_client()

    @pytest.fixture
    def valid_parked_parking(self):
        return {
            'plate': 'GDF8F62',
            'brand': 'volkswagen',
            'model': 'gol',
            'color': 'black',
            'status': 'parked'
        }

    @pytest.fixture
    def valid_left_parking(self):
        return {
            'plate': 'GDF8F62',
            'brand': 'volkswagen',
            'model': 'gol',
            'color': 'black',
            'status': 'left'
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
    def sample_parking_uuid(self, client, valid_parked_parking):
        response = client.post('/parking', json=valid_parked_parking)
        return response.json['uuid']

    def test_get_parkings(self, client):
        response = client.get('/parkings')
        assert response.status_code == 200

    def test_get_parking(self, client, sample_parking_uuid):
        response = client.get(f'/parking/{sample_parking_uuid}')
        assert response.status_code == 200
        assert response.json['plate'] == 'GDF8F62'
        assert response.json['brand'] == 'volkswagen'
        assert response.json['model'] == 'gol'
        assert response.json['color'] == 'black'
        assert response.json['status'] == 'parked'
        assert response.json['entry'] is not None
        assert response.json.get('exit') is None
        assert response.json.get('total_amount') is None

        response = client.get('/parking/00000000-0000-0000-0000-000000000000')
        assert response.status_code == 404
        assert b'Parking not found.' in response.data

    def test_post_parking(
        self, client, valid_parked_parking, valid_left_parking, invalid_parking
    ):

        # Testing valid parked parking
        response = client.post('/parking', json=valid_parked_parking)
        assert response.status_code == 201
        assert response.json['plate'] == 'GDF8F62'
        assert response.json['brand'] == 'volkswagen'
        assert response.json['model'] == 'gol'
        assert response.json['color'] == 'black'
        assert response.json['entry'] is not None
        assert response.json['status'] == 'parked'
        assert response.json.get('exit') is None
        assert response.json.get('total_amount') is None

        # Testing valid left parking
        response = client.post('/parking', json=valid_left_parking)
        assert response.status_code == 201
        assert response.json['plate'] == 'GDF8F62'
        assert response.json['brand'] == 'volkswagen'
        assert response.json['model'] == 'gol'
        assert response.json['color'] == 'black'
        assert response.json['entry'] is not None
        assert response.json['status'] == 'left'
        assert response.json.get('exit') is not None
        assert response.json.get('total_amount') == 0.0

        # Testing invalid parking
        response = client.post('/parking', json=invalid_parking)
        assert response.status_code == 400
        assert b'This field cannot be blank.' in response.data

    def test_put_parking(
        self, client, sample_parking_uuid, valid_left_parking
    ):
        response = client.put(
            f'/parking/{sample_parking_uuid}', json=valid_left_parking
        )
        assert response.status_code == 201
        assert response.json['plate'] == 'GDF8F62'
        assert response.json['brand'] == 'volkswagen'
        assert response.json['model'] == 'gol'
        assert response.json['color'] == 'black'
        assert response.json['entry'] is not None
        assert response.json['status'] == 'left'
        assert response.json.get('exit') is not None
        assert response.json.get('total_amount') == 0.0

    def test_delete_parking(self, client, sample_parking_uuid):
        response = client.delete(f'/parking/{sample_parking_uuid}')
        assert response.status_code == 204
