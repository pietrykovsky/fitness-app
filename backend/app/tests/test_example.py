from app.tests.conftest import client


def test_create_user():
    response = client.post(
        "api/users/open",
        json={"email": "deadpool@example.com", "first_name": "john", "last_name": "doe", "password": "chimichangas4life"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert "id" in data
