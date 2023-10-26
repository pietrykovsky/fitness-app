import pytest

from app.crud import user as user_crud
from app.tests import const


@pytest.mark.parametrize("payload", const.SAMPLE_USER_DATA)
def test_user_creation_success(payload, client, db_session):
    response = client.post(const.USER_CREATE_OPEN_URL, json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data

    user = user_crud.get(db_session, email=payload["email"])
    assert user is not None
    assert user.email == payload["email"]
