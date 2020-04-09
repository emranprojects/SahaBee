import requests

API_URL = 'http://localhost:8000'

def service_available():
    response = requests.get(API_URL)
    assert response.status_code == 200