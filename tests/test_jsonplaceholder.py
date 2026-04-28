import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_single_post_status_code():
    """Test that GET /posts/1 returns a 200 status code."""
    response = requests.get(f"{BASE_URL}/posts/1")
    assert response.status_code == 200

def test_get_single_post_content():
    """Test that GET /posts/1 returns expected content."""
    response = requests.get(f"{BASE_URL}/posts/1")
    data = response.json()
    assert data['id'] == 1
    assert 'title' in data
    assert 'body' in data
    assert 'userId' in data

def test_create_new_post():
    """Test that a POST request to /posts creates a new post and returns 201 status code."""
    new_post_data = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }
    response = requests.post(f"{BASE_URL}/posts", json=new_post_data)
    assert response.status_code == 201
    data = response.json()
    assert data['title'] == "foo"
    assert data['body'] == "bar"
    assert data['userId'] == 1
    assert 'id' in data # The API should assign a new ID

def test_update_existing_post():
    """Test that a PUT request to /posts/1 updates a post and returns a 200 status code."""
    updated_post_data = {
        "id": 1,
        "title": "updated title",
        "body": "updated body",
        "userId": 1
    }
    response = requests.put(f"{BASE_URL}/posts/1", json=updated_post_data)
    assert response.status_code == 200
    data = response.json()
    assert data['title'] == "updated title"
    assert data['body'] == "updated body"
    assert data['id'] == 1

def test_delete_existing_post():
    """Test that a DELETE request to /posts/1 deletes a post and returns a 200 status code."""
    response = requests.delete(f"{BASE_URL}/posts/1")
    assert response.status_code == 200
    # For JSONPlaceholder, a successful delete usually returns an empty object {}
