import pytest
import os
import sys
sys.path.insert(0, os.getcwd())
from app.app import create_app


expected_fields = ['author', 'authorId', 'id', 'likes', 'popularity', 'reads', 'tags']

@pytest.fixture
def client():
    app = create_app()

    with app.test_client() as client:
        yield client

def test_api_ping(client):
    ping = client.get('/api/ping')
    json_data = ping.get_json()
    assert 'success' in json_data.keys()
    assert True in json_data.values()
    assert ping.status_code == 200


def test_get_api_post_with_valid_tag(client):
    get = client.get('/api/posts?tags=tech')
    json_data = get.get_json()
    assert get.status_code == 200
    assert len(json_data[0].keys()) == len(expected_fields)
    assert all([a == b for a, b in zip(json_data[0].keys(), expected_fields)])

def test_get_api_post_with_multiple_valid_tag(client):
    get = client.get('/api/posts?tags=tech,health')
    json_data = get.get_json()
    assert get.status_code == 200
    assert len(json_data[0].keys()) == len(expected_fields)
    assert all([a == b for a, b in zip(json_data[0].keys(), expected_fields)])

def test_get_api_post_with_invalid_tag(client):
    get = client.get('/api/posts?tags=')
    json_data = get.get_json()
    assert get.status_code != 200
    assert 'error' in json_data.keys()

def test_get_api_post_with_valid_sortby(client):
    get = client.get('/api/posts?tags=tech&sortBy=likes')
    json_data = get.get_json()
    likes = []
    for post in json_data:
        likes.append(post['likes'])
    assert get.status_code == 200
    assert len(json_data[0].keys()) == len(expected_fields)
    assert all([a == b for a, b in zip(likes, sorted(likes))])

def test_get_api_post_with_invalid_sortby(client):
    get = client.get('/api/posts?tags=tech&sortBy=no')
    json_data = get.get_json()
    assert get.status_code != 200
    assert 'error' in json_data.keys()

def test_get_api_post_with_valid_direction(client):
    get = client.get('/api/posts?tags=tech&sortBy=likes&direction=desc')
    json_data = get.get_json()
    likes = []
    for post in json_data:
        likes.append(post['likes'])
    assert get.status_code == 200
    assert len(json_data[0].keys()) == len(expected_fields)
    assert all([a == b for a, b in zip(likes, sorted(likes, reverse=True))])

def test_get_api_post_with_invalid_direction(client):
    get = client.get('/api/posts?tags=tech&sortBy=likes&direction=no')
    json_data = get.get_json()
    assert get.status_code != 200
    assert 'error' in json_data.keys()