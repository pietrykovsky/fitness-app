import logging
from sqlalchemy.orm import Session

from app.core.database import Base
from app.models import User


LOG = logging.getLogger(__name__)


def assert_user_properties(user: User, expected: dict):
    """
    Assert the properties of a user model against an expected dictionary.

    :param user: The user instance to check.
    :param expected: The dictionary with expected values.
    """
    assert user.id is not None, f"User ID should not be None!"
    assert (
        user.email == expected["email"]
    ), f"Actual email \"{user.email}\" does not match with expected \"{expected['email']}\""
    assert (
        user.first_name == expected["first_name"]
    ), f"Actual first name \"{user.first_name}\" does not match with expected \"{expected['first_name']}\""
    assert (
        user.last_name == expected["last_name"]
    ), f"Actual last name \"{user.last_name}\" does not match with expected \"{expected['last_name']}\""
    assert (
        user.password == expected["password"]
    ), f"Actual password \"{user.password}\" does not match with expected \"{expected['password']}\""
    assert user.is_superuser is False, "User should not be a superuser by default!"
    assert user.is_active is True, "User should be active by default!"
    assert user.create_date is not None, "User create date should not be None!"


def add_model_to_db(db_session: Session, model: Base, data: dict) -> Base:
    """
    Add a model instance to the database and return it.

    :param db_session: The database session to use for adding the model.
    :param model: The model class to use for adding the model.
    :param data: The data for the model to be added.
    :return: The added model instance.
    """
    instance = model(**data)
    db_session.add(instance)
    db_session.commit()
    LOG.debug(f"Added model to database: {instance}")
    return instance
