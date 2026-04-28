
import pytest
from .client import APIClient

BASE_URL = "https://api.agify.io"
client = APIClient(BASE_URL)

def test_agify_status_code_success():
    """Test that GET /?name=michael returns a 200 status code."""
    response, latency = client.get("/?name=michael")
    assert response.status_code == 200
    return latency

def test_agify_response_content_michael():
    """Test that GET /?name=michael returns expected content."""
    response, latency = client.get("/?name=michael")
    data = response.json()
    assert 'name' in data
    assert data['name'] == 'michael'
    assert 'age' in data
    assert isinstance(data['age'], int)
    assert 'count' in data
    assert isinstance(data['count'], int)
    return latency

def test_agify_response_content_invalid_name():
    """Test that GET /?name=123 (invalid name) returns expected content."""
    response, latency = client.get("/?name=123")
    data = response.json()
    assert data['name'] == '123'
    assert data['age'] is None
    assert isinstance(data['count'], int)
    return latency

def test_agify_no_name_parameter():
    """Test that GET / (no name) returns 422 status code."""
    response, latency = client.get("/")
    assert response.status_code == 422
    data = response.json()
    assert 'error' in data
    assert data['error'] == 'Missing "name" parameter'
    return latency

def test_agify_multiple_names_status_code():
    """Test that GET /?name[]=michael&name[]=matthias returns 200 status code."""
    response, latency = client.get("/?name[]=michael&name[]=matthias")
    assert response.status_code == 200
    return latency

def test_agify_multiple_names_content():
    """Test that GET /?name[]=michael&name[]=matthias returns list of expected content."""
    response, latency = client.get("/?name[]=michael&name[]=matthias")
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    for item in data:
        assert 'name' in item
        assert 'age' in item
        assert isinstance(item['count'], int)
    assert data[0]['name'] == 'michael'
    assert data[1]['name'] == 'matthias'
    return latency
