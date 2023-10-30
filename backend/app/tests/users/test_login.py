import logging

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests import const
from app.crud import user as user_crud
from app.schemas import UserCreate


LOG = logging.getLogger(__name__)


def test_login_access_token(client: TestClient, db_session: Session):
    """
    Test the login access token endpoint.

    Requirements:
        - Database session is provided.
        - Client has been initialized.

    Steps:
        1. Add a user to the database.
        2. Attempt to login with the user's credentials.
        3. Check that the response contains an access token.

    Pass criteria:
        Response contains an access token.
    """
    user_data = const.SAMPLE_USER_DATA[0]
    user_crud.create(db=db_session, obj_in=UserCreate(**user_data))
    LOG.debug(f"Created and added user to database: {user_data}")
    payload = {"username": user_data["email"], "password": user_data["password"]}
    response = client.post(const.LOGIN_URL, data=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data, f"Access token not found in response: {data}"
    assert "token_type" in data, f"Token type not found in response: {data}"
    assert (
        data["token_type"] == "bearer"
    ), f"Actual token type \"{data['token_type']}\" does not match expected \"bearer\""
