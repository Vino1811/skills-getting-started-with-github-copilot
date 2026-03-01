"""
Tests for the root endpoint (GET /).

This test module verifies that the root endpoint redirects users to the static
HTML interface as expected.
"""


def test_root_redirect(client):
    """
    Test that GET / redirects to /static/index.html.
    
    The root endpoint should return a 307 (temporary redirect) response
    pointing users to the main UI.
    
    Args:
        client: FastAPI TestClient fixture
    """
    response = client.get("/", follow_redirects=False)
    
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_follows(client):
    """
    Test that following the root redirect returns the HTML page.
    
    Args:
        client: FastAPI TestClient fixture
    """
    response = client.get("/", follow_redirects=True)
    
    # The static file should be served successfully
    assert response.status_code == 200
