from fastapi.testclient import TestClient
from main import app

test_client = TestClient(app)

# test GET /
def test_get_root():
    response = test_client.get("/")
    assert response.status_code == 200
    
# test GET /hola/sencillo
def test_get_hola_sencillo():
    response = test_client.get("/hola/sencillo")
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/json"
    assert response.json().get("msg") == "Hola Mundo!"
    
# test GET /hola/hola-si-hay-alguien true
def test_get_hola_si_hay_alguien_true():
    response = test_client.get("/hola/hola-si-hay-alguien?alguien=true")
    print(response.text)
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/json"
    assert response.json().get("msg") == "Hola, porque hay alguien!"
    
# test GET /hola/hola-si-hay-alguien false
def test_get_hola_si_hay_alguien_false():
    response = test_client.get("/hola/hola-si-hay-alguien?alguien=false")
    print(response.text)
    assert response.status_code == 404
    assert response.headers.get("content-type") == "application/json"
    assert response.json().get("msg") == "No hay nadie"
    
    
# test GET /hola/hola-si-hay-alguien error
def test_get_hola_si_hay_alguien_error():
    response = test_client.get("/hola/hola-si-hay-alguien")
    print(response.text)
    assert response.status_code == 422
    assert response.headers.get("content-type") == "application/json"
    assert response.json().get("detail")[0].get("msg") == "Field required"