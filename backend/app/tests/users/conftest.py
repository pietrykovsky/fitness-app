import pytest
from sqlalchemy.orm import Session

from app.models import User
from app.tests.utils import add_user_to_db


@pytest.fixture(scope="function")
def create_user_model(
    request: pytest.FixtureRequest, db_session: Session
) -> tuple[User, dict]:
    """
    Create a user model using the provided request parameters and return the user and its data.

    :param request: The pytest request object with test parameters.
    :param db_session: The database session.
    :return: A tuple containing the user model and its expected data.
    """
    user = add_user_to_db(db_session, request.param)
    return user, request.param
