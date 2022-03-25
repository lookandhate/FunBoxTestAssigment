import time

from fastapi.testclient import TestClient
import json
from main import app
import os
os.environ['REDIS_HOST'] = 'localhost'
os.environ['REDIS_PORT'] = '6379'

def test_post_request():
    with TestClient(app) as client:
        response = client.post('/visited_links', json={'links': ['ya.ru?q=123']})
        assert response.status_code == 200
        assert response.json()['status'] == 'ok'


def test_data_saves_to_db():
    with TestClient(app) as client:
        current_time = int(time.time())
        delta_time = 1000

        post_request = client.post('/visited_links',
                                   json={'links': ['ya.ru?q=123', 'funbox.com?q=1337', 'https://go.dev/solutions/']})
        assert post_request.status_code == 200
        assert post_request.json()['status'] == 'ok'

        get_request = client.get(
            f'/visited_domains?from_timestamp={current_time - delta_time}&to={current_time + delta_time}')
        assert get_request.status_code == 200
        assert get_request.json()['status'] == 'ok'
        assert all([domain in get_request.json()['domains'] for domain in ['ya.ru', 'funbox.com', 'go.dev']])
