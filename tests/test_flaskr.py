from app import app
import requests
def test_home_route():
    response = app.test_client().get('/')
    assert response.status_code == 200

def test_list_route():
    response = app.test_client().get('/list')
    assert response.status_code == 200





