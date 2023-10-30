import logging
from typing import Any
from sqlalchemy.orm import Session

from app.models import User


LOG = logging.getLogger(__name__)


def assert_properties(actual: dict | Any, expected: dict | Any):
    """
    Assert the properties of an object against an expected dictionary.

    :param actual: The actual object to check.
    :param expected: The dictionary with expected values.
    """
    actual_dict = vars(actual) if not isinstance(actual, dict) else actual
    expected_dict = vars(expected) if not isinstance(expected, dict) else expected

    expected_attrs = [
        key
        for key in expected_dict
        if not callable(getattr(expected, key)) and not key.startswith("_")
    ]
    for key in expected_attrs:
        assert key in actual_dict, f"Attribute '{key}' not found in actual object"
        assert getattr(actual, key) == getattr(
            expected, key
        ), f"Value for attribute '{key}' does not match. Expected: '{getattr(expected, key)}', Got: '{getattr(actual, key)}'"


def assert_user_properties(user: User, expected: dict):
    """
    Assert the properties of a user model against an expected dictionary.

    :param user: The user instance to check.
    :param expected: The dictionary with expected values.
    """
    assert user.id is not None
    assert user.email == expected["email"]
    assert user.first_name == expected["first_name"]
    assert user.last_name == expected["last_name"]
    assert user.password == expected["password"]
    assert user.is_superuser is False
    assert user.is_active is True
    assert user.create_date is not None


def add_user_to_db(db_session: Session, user_data: dict) -> User:
    """
    Add a user instance to the database and return it.

    :param db_session: The database session to use for adding the user.
    :param user_data: The data for the user to be added.
    :return: The added user instance.
    """
    user = User(**user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    LOG.debug(f"Added user to database: {user}")
    return user
