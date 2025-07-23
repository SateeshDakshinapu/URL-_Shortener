import pytest
from app.main import app
from app.utils import generate_short_code

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_shorten_url_valid(client):
    response = client.post('/shorten', json={'url': 'https://www.google.com'})
    assert response.status_code == 201
    assert 'short_url' in response.get_json()

def test_shorten_url_invalid(client):
    response = client.post('/shorten', json={'url': 'bad_url'})
    assert response.status_code == 400

def test_shorten_url_missing(client):
    response = client.post('/shorten', json={})
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_redirect_and_analytics(client):
    # Shorten a URL
    post_resp = client.post('/shorten', json={'url': 'https://example.com'})
    short_url = post_resp.get_json()['short_url']
    short_code = short_url.split('/')[-1]

    # Redirect
    redirect_resp = client.get(f'/r/{short_code}')
    assert redirect_resp.status_code == 302
    assert 'Location' in redirect_resp.headers

    # Analytics
    analytics_resp = client.get(f'/analytics/{short_code}')
    assert analytics_resp.status_code == 200
    data = analytics_resp.get_json()
    assert data['original_url'] == 'https://example.com'
    assert 'clicks' in data

def test_redirect_invalid_code(client):
    response = client.get('/r/invalid123')
    assert response.status_code == 404

def test_analytics_invalid_code(client):
    response = client.get('/analytics/invalid123')
    assert response.status_code == 404
