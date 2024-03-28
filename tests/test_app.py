import pytest
from src import create_app


class TestApplication():

    @pytest.fixture
    def client(self):
        app = create_app('config.MockConfig')
        return app.test_client()

    def test_get_parkings(self, client):
        response = client.get('/parkings')
        assert response.status_code == 200
