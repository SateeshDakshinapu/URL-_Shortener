import pytest
from app.main import app
from app.utils import validate_url, generate_short_code

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_shorten_and_redirect(client):
    # Test POST to /shorten
    response = client.post('/shorten', json={'url': 'https://example.com'})
    assert response.status_code == 201
    json_data = response.get_json()
    assert 'short_url' in json_data

    short_url = json_data['short_url']
    short_code = short_url.split('/r/')[-1]

    # Test redirect works
    redirect_response = client.get(f'/r/{short_code}')
    assert redirect_response.status_code == 302
    assert redirect_response.location == 'https://example.com'

def test_invalid_url(client):
    response = client.post('/shorten', json={'url': 'invalid-url'})
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_missing_url(client):
    response = client.post('/shorten', json={})
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_analytics(client):
    # Shorten a URL
    shorten_resp = client.post('/shorten', json={'url': 'https://example.com'})
    assert shorten_resp.status_code == 201
    short_code = shorten_resp.get_json()['short_url'].split('/r/')[-1]

    # Click the shortened URL
    client.get(f'/r/{short_code}')

    # Fetch analytics
    analytics_resp = client.get(f'/analytics/{short_code}')
    data = analytics_resp.get_json()

    assert analytics_resp.status_code == 200
    assert data['original_url'] == 'https://example.com'
    assert data['clicks'] == 1
    assert isinstance(data['access_timestamps'], list)

def test_redirect_invalid_code(client):
    response = client.get('/r/nonexistent')
    assert response.status_code == 404
    assert 'error' in response.get_json()

def test_analytics_invalid_code(client):
    response = client.get('/analytics/nonexistent')
    assert response.status_code == 404
    assert 'error' in response.get_json()

# === Additional Tests for utils.py ===

def test_validate_url_valid():
    assert validate_url("https://www.google.com")
    assert validate_url("http://example.org")

def test_validate_url_invalid():
    assert not validate_url("htp://invalid-url")
    assert not validate_url("justtext")

def test_generate_short_code():
    code1 = generate_short_code()
    code2 = generate_short_code()
    assert isinstance(code1, str)
    assert len(code1) == 6  # Default length
    assert code1 != code2  # Very unlikely to be equal
