import pytest
import logging
from fastapi import FastAPI
from sqlalchemy.orm import Session

from app.models import User
from app.tests.utils import add_user_to_db
from app.core.deps import get_current_user


LOG = logging.getLogger(__name__)


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


@pytest.fixture(scope="function")
def override_get_current_user(create_user_model, app: FastAPI):
    """Override the get_db dependency to use the test database."""
    user, _ = create_user_model

    def _get_current_user_override():
        return user

    app.dependency_overrides[get_current_user] = _get_current_user_override
    LOG.debug("Overridden `get_current_user` dependency.")
    yield user
    app.dependency_overrides.pop(get_current_user, None)
    LOG.debug("Restored `get_current_user` dependency.")


@pytest.fixture(scope="function")
def get_current_superuser(override_get_current_user, db_session):
    override_get_current_user.is_superuser = True
    db_session.commit()
    db_session.refresh(override_get_current_user)
    LOG.debug("Set current user as superuser.")
    return override_get_current_user
