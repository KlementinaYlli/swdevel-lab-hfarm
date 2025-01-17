"""
Execute this test by running on the terminal (from the app/) the command:
pytest --cov=app --cov-report=html tests/
"""

import os
import sys
from fastapi.testclient import TestClient

# Add the project root to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can do the relative import
from app.main import app

client = TestClient(app)

def test_search_valid():
    """
    Tests a valid request to backend.

    Checks the status code and the quality of the response.
    """

    response = client.get("/module/search/rank/treviso/istituto comprensivo")
    assert response.status_code == 200
    assert response is not None
    assert len(response.json()['result']) != 0
    
def test_search_empty():
    """
    Tests an empty request to the backend.

    Checks the status code and verifies that no results are returned.
    """

    # Conegliano is not a province
    response = client.get("/module/search/rank/parigi/istituto comprensivo")
    assert response.status_code == 200
    assert response is not None
    assert response.json() == {'error': "Unable to find school"}

def test_search_edge():
    """
    Tests an invalid request to the backend.

    Checks the status code and verifies that the no valid result is found.
    """

    # Invalid input request.
    response = client.get("/module/search/rank/1134w/istitu578to compr()ensivo")
    assert response.status_code == 200
    assert response is not None
    assert response.json() == {'error': "Unable to find school"}