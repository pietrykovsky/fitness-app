from sqlalchemy.orm import Session

from app.models import User


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
    return user
