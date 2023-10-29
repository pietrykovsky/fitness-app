import pytest
from app.crud import user as user_crud
from app.tests import const
from app.tests.utils import add_user_to_db


@pytest.mark.parametrize("payload", const.SAMPLE_USER_DATA[1:2])
def test_user_create_open_success(payload, client, db_session):
    response = client.post(const.USER_CREATE_OPEN_URL, json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data

    user = user_crud.get(db_session, email=payload["email"])
    assert user is not None
    assert user.email == payload["email"]


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
def test_retrieve_me_success(override_get_current_user, client):
    expected = override_get_current_user
    response = client.get(const.USER_ME_URL)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == expected.id
    assert data["email"] == expected.email
    assert data["first_name"] == expected.first_name
    assert data["last_name"] == expected.last_name
    assert data["is_active"] == expected.is_active
    assert data["is_superuser"] == expected.is_superuser
    assert data["create_date"] == expected.create_date.isoformat()


def test_retrieve_me_failure(client):
    response = client.get(const.USER_ME_URL)
    assert response.status_code == 401, response.text


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
def test_update_me_success(override_get_current_user, client, db_session):
    user = override_get_current_user
    payload = {
        "first_name": "new first name",
        "last_name": "new last name",
    }
    response = client.put(const.USER_ME_URL, json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    db_session.refresh(user)
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert user.first_name == payload["first_name"]
    assert user.last_name == payload["last_name"]


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
@pytest.mark.usefixtures("get_current_superuser")
def test_create_user_success(client, db_session):
    payload = const.SAMPLE_USER_DATA[1]
    response = client.post(const.USER_URL, json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data

    user = user_crud.get(db_session, email=payload["email"])
    assert user is not None
    assert user.email == payload["email"]


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
@pytest.mark.usefixtures("get_current_superuser")
def test_update_user_success(client, db_session):
    user = add_user_to_db(db_session, const.SAMPLE_USER_DATA[1])
    payload = {
        "first_name": "new first name",
        "last_name": "new last name",
    }
    response = client.put(f"{const.USER_URL}/{user.id}", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    db_session.refresh(user)
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert user.first_name == payload["first_name"]
    assert user.last_name == payload["last_name"]


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
@pytest.mark.usefixtures("get_current_superuser")
def test_read_users_success(client, db_session):
    for user in const.SAMPLE_USER_DATA[1:]:
        add_user_to_db(db_session, user)
    response = client.get(const.USER_URL)
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == len(const.SAMPLE_USER_DATA)
