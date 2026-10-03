import sys

# Allow Python to find main.py inside Server
sys.path.insert(0, "Server")
from main import app, inventory
def setup_function():
    # Clear inventory before every test
    inventory.clear()

# HOME
def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

# LOGIN
def test_login():

    client = app.test_client()

    response = client.post(
        "/login",
        json={
            "username": "benson",
            "password": "12345"
        } )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Login successful"

#  CREATE ITEM
def test_create_item(monkeypatch):
    # Fake external API
    class FakeResponse:
        status_code = 200
        def json(self):
            return {
                "status": 1,
                "product": {
                    "product_name": "Coca Cola",
                    "brands": "Coca Cola"
                }}
            

    def fake_get(*args, **kwargs):
        return FakeResponse()
    monkeypatch.setattr(
        "main.requests.get",
        fake_get
    )
    client = app.test_client()
    response = client.post(
        "/inventory",
        json={
            "code": "123456",
            "quantity": 10
        }
    )
    assert response.status_code == 201
    assert len(inventory) == 1
    assert inventory[0]["name"] == "Coca Cola"

# GET INVENTORY
def test_get_inventory():
    inventory.append({
        "id": 1,
        "code": "123",
        "name": "Milk",
        "brand": "Brookside",
        "quantity": 20,
        "expiration": None
    })
    client = app.test_client()
    response = client.get(
        "/inventory"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["count"] == 1

#  UPDATE ITEM
def test_update_item():
    inventory.append({
        "id": 1,
        "code": "123",
        "name": "Milk",
        "brand": "Brookside",
        "quantity": 20,
        "expiration": None
    })
    client = app.test_client()
    response = client.patch(
        "/inventory/1",
        json={
            "quantity": 50
        }
    )
    assert response.status_code == 200
    assert inventory[0]["quantity"] == 50

#  DELETE ITEM
def test_delete_item():
    inventory.append({
        "id": 1,
        "code": "123",
        "name": "Milk",
        "brand": "Brookside",
        "quantity": 20,
        "expiration": None
    })

    client = app.test_client()
    response = client.delete(
        "/inventory/1"
    )
    assert response.status_code == 200
    assert len(inventory) == 0

 #EXTERNAL API SEARCH
def test_search_product(monkeypatch):
    class FakeResponse:
        status_code = 200
        text = '{"status": 1, "product": {"product_name": "Coca Cola"}}'
        def json(self):
            return {
                "status": 1,
                "product": {
                    "product_name": "Coca Cola",
                    "brands": "Coca Cola"
                }}
            
    def fake_get(*args, **kwargs):
        return FakeResponse()
    monkeypatch.setattr(
        "main.requests.get",
        fake_get
    )
    client = app.test_client()
    response = client.get(
        "/search/123456"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Coca Cola"
#COOKIE
def test_cookie():
    client = app.test_client()
    response = client.get(
        "/set_cookie"
    )
    assert response.status_code == 200
    response = client.get(
        "/get_cookie"
    )
    assert response.status_code == 200
