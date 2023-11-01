import pytest
import logging
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import user as user_crud
from app.models import User
from app.tests import const
from app.tests.utils import add_model_to_db


LOG = logging.getLogger(__name__)


@pytest.mark.parametrize("payload", const.SAMPLE_USER_DATA[1:2])
def test_user_create_open_success(
    payload: dict, client: TestClient, db_session: Session
):
    """
    Test successfully creating a new user via the open endpoint.

    Requirements:
        - The provided user data is valid.

    Steps:
        1. Send a POST request with user data to the open user creation endpoint.
        2. Assert that the response is successful and contains the expected data.
        3. Retrieve the user from the database and verify the saved data.

    Pass criteria:
        - The user data returned in the response matches the provided data.
        - The user is saved in the database with the provided data.
    """
    response = client.post(const.USER_CREATE_OPEN_URL, json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert (
        data["email"] == payload["email"]
    ), f"Actual email \"{data['email']}\" does not match expected \"{payload['email']}\""
    assert "id" in data, f"ID not found in response: {data}"

    user = user_crud.get(db_session, email=payload["email"])
    assert user is not None, f"User not found in database: {payload}"
    assert (
        user.email == payload["email"]
    ), f"Actual email \"{user.email}\" does not match expected \"{payload['email']}\""


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
def test_retrieve_me_success(override_get_current_user: User, client: TestClient):
    """
    Test successfully retrieving the current authenticated user's data.

    Requirements:
        - A user is authenticated.

    Steps:
        1. Send a GET request to the "me" endpoint.
        2. Assert that the response is successful and contains the expected user data.

    Pass criteria:
        - The user data returned in the response matches the authenticated user's data.
    """
    expected = override_get_current_user
    response = client.get(const.USER_ME_URL)
    assert response.status_code == 200, response.text
    data = response.json()
    assert (
        data["id"] == expected.id
    ), f"Actual ID \"{data['id']}\" does not match expected \"{expected.id}\""
    assert (
        data["email"] == expected.email
    ), f"Actual email \"{data['email']}\" does not match expected \"{expected.email}\""
    assert (
        data["first_name"] == expected.first_name
    ), f"Actual first name \"{data['first_name']}\" does not match expected \"{expected.first_name}\""
    assert (
        data["last_name"] == expected.last_name
    ), f"Actual last name \"{data['last_name']}\" does not match expected \"{expected.last_name}\""
    assert (
        data["is_active"] == expected.is_active
    ), f"Actual is_active \"{data['is_active']}\" does not match expected \"{expected.is_active}\""
    assert (
        data["is_superuser"] == expected.is_superuser
    ), f"Actual is_superuser \"{data['is_superuser']}\" does not match expected \"{expected.is_superuser}\""
    assert (
        data["create_date"] == expected.create_date.isoformat()
    ), f"Actual create_date \"{data['create_date']}\" does not match expected \"{expected.create_date.isoformat()}\""


def test_retrieve_me_failure(client: TestClient):
    """
    Test failure when trying to retrieve data for a non-authenticated user.

    Requirements:
        - No user is authenticated.

    Steps:
        1. Send a GET request to the "me" endpoint without authentication.
        2. Assert that the response returns a 401 Unauthorized status.

    Pass criteria:
        - The server responds with a 401 Unauthorized status.
    """
    response = client.get(const.USER_ME_URL)
    assert response.status_code == 401, response.text


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
def test_update_me_success(
    override_get_current_user: User, client: TestClient, db_session: Session
):
    """
    Test successfully updating the current authenticated user's data.

    Requirements:
        - A user is authenticated.

    Steps:
        1. Send a PUT request to the "me" endpoint with updated data.
        2. Assert that the response is successful and contains the updated user data.
        3. Verify that the user's data in the database has been updated.

    Pass criteria:
        - The user data returned in the response and in the database matches the updated data.
    """
    user = override_get_current_user
    payload = {
        "first_name": "new first name",
        "last_name": "new last name",
    }
    response = client.put(const.USER_ME_URL, json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    db_session.refresh(user)
    LOG.debug("Refreshed database.")
    assert (
        data["first_name"] == payload["first_name"]
    ), f"Actual first name \"{data['first_name']}\" does not match expected \"{payload['first_name']}\""
    assert (
        data["last_name"] == payload["last_name"]
    ), f"Actual last name \"{data['last_name']}\" does not match expected \"{payload['last_name']}\""
    assert (
        user.first_name == payload["first_name"]
    ), f"Actual first name \"{user.first_name}\" does not match expected \"{payload['first_name']}\""
    assert (
        user.last_name == payload["last_name"]
    ), f"Actual last name \"{user.last_name}\" does not match expected \"{payload['last_name']}\""


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
@pytest.mark.usefixtures("get_current_superuser")
def test_create_user_success(client: TestClient, db_session: Session):
    """
    Test successfully creating a new user.

    Requirements:
        - The current user has superuser privileges.
        - The provided user data is valid.

    Steps:
        1. Send a POST request with user data to the user creation endpoint.
        2. Assert that the response is successful and contains the expected user data.
        3. Retrieve the user from the database and verify the saved data.

    Pass criteria:
        - The user data returned in the response matches the provided data.
        - The user is saved in the database with the provided data.
    """
    payload = const.SAMPLE_USER_DATA[1]
    response = client.post(const.USER_URL, json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert (
        data["email"] == payload["email"]
    ), f"Actual email \"{data['email']}\" does not match expected \"{payload['email']}\""
    assert "id" in data, f"ID not found in response: {data}"

    user = user_crud.get(db_session, email=payload["email"])
    assert user is not None, f"User not found in database: {payload}"
    assert (
        user.email == payload["email"]
    ), f"Actual email \"{user.email}\" does not match expected \"{payload['email']}\""


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
@pytest.mark.usefixtures("get_current_superuser")
def test_update_user_success(client: TestClient, db_session: Session):
    """
    Test successfully updating a specific user's data.

    Requirements:
        - The current user has superuser privileges.
        - The user to be updated exists in the system.

    Steps:
        1. Send a PUT request with updated data to the specific user's endpoint.
        2. Assert that the response is successful and contains the updated user data.
        3. Retrieve the user from the database and verify the updated data.

    Pass criteria:
        - The user data returned in the response and in the database matches the updated data.
    """
    user = add_model_to_db(db_session, User, const.SAMPLE_USER_DATA[1])
    payload = {
        "first_name": "new first name",
        "last_name": "new last name",
    }
    response = client.put(f"{const.USER_URL}/{user.id}", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    db_session.refresh(user)
    LOG.debug("Refreshed database.")
    assert (
        data["first_name"] == payload["first_name"]
    ), f"Actual first name \"{data['first_name']}\" does not match expected \"{payload['first_name']}\""
    assert (
        data["last_name"] == payload["last_name"]
    ), f"Actual last name \"{data['last_name']}\" does not match expected \"{payload['last_name']}\""
    assert (
        user.first_name == payload["first_name"]
    ), f"Actual first name \"{user.first_name}\" does not match expected \"{payload['first_name']}\""
    assert (
        user.last_name == payload["last_name"]
    ), f"Actual last name \"{user.last_name}\" does not match expected \"{payload['last_name']}\""


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
@pytest.mark.usefixtures("get_current_superuser")
def test_read_users_success(client: TestClient, db_session: Session):
    """
    Test successfully retrieving a list of all users.

    Requirements:
        - Multiple users exist in the system.
        - The current user has superuser privileges.

    Steps:
        1. Send a GET request to the users list endpoint.
        2. Assert that the response is successful and contains a list of user data.
        3. Compare the number of users in the response with the expected number.

    Pass criteria:
        - The number of users in the response matches the expected number.
        - The user data in the response matches the users in the system.
    """
    for user in const.SAMPLE_USER_DATA[1:]:
        add_model_to_db(db_session, User, user)
    response = client.get(const.USER_URL)
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == len(
        const.SAMPLE_USER_DATA
    ), f'Actual number of users "{len(data)}" does not match expected "{len(const.SAMPLE_USER_DATA)}"'
