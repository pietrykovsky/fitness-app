import pytest
import logging
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from app.models import User
from app.tests import const
from app.tests.utils import assert_user_properties, add_user_to_db


LOG = logging.getLogger(__name__)


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
def test_create_user_success(create_user_model: tuple[User, dict]):
    """
    Test successful creation of a user.

    Requirements:
        - User data is passed as a parameter.

    Steps:
        1. Create a user with the provided data.
        2. Assert properties of the user against the provided data.

    Pass criteria:
        User properties match the provided data.
    """
    user, expected = create_user_model
    assert_user_properties(user, expected)


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
def test_get_user_success(create_user_model: tuple[User, dict], db_session: Session):
    """
    Test successful retrieval of a user from the database.

    Requirements:
        - User is previously created in the database.

    Steps:
        1. Retrieve a user with the known ID from the database.
        2. Assert properties of the retrieved user against the known data.

    Pass criteria:
        - User properties match the known data.
    """
    user, expected = create_user_model
    assert user is not None, "User should not be None!"

    user = db_session.execute(select(User).filter(User.id == user.id)).scalar_one()
    assert_user_properties(user, expected)


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
def test_update_user_success(create_user_model: tuple[User, dict], db_session: Session):
    """
    Test successful update of a user's properties.

    Requirements:
        - User is previously created in the database.

    Steps:
        1. Update known properties of the user.
        2. Persist the changes to the database.
        3. Assert updated properties of the user.

    Pass criteria:
        - Updated user properties match the new data.
    """
    NEW_PASSWORD = "new_password"
    NEW_LAST_NAME = "new_last_name"

    user, expected = create_user_model
    assert user is not None, "User should not be None!"
    assert (
        user.password == expected["password"]
    ), f"Acutal password \"{user.password}\" does not match with expected \"{expected['password']}\""
    assert (
        user.last_name == expected["last_name"]
    ), f"Acutal last name \"{user.last_name}\" does not match with expected \"{expected['last_name']}\""

    expected["password"] = NEW_PASSWORD
    expected["last_name"] = NEW_LAST_NAME
    LOG.debug(f"Updated expected data: {expected}")

    user.password = NEW_PASSWORD
    user.last_name = NEW_LAST_NAME
    db_session.commit()
    db_session.refresh(user)
    LOG.debug(f"Commited changes and refresh database.")

    assert_user_properties(user, expected)


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
def test_delete_user_success(create_user_model: tuple[User, dict], db_session: Session):
    """
    Test successful deletion of a user from the database.

    Requirements:
        - User is previously created in the database.

    Steps:
        1. Delete the user from the database.
        2. Try to retrieve the user by its ID.

    Pass criteria:
        - User is not found in the database.
    """
    user, _ = create_user_model
    assert user.id is not None, "User ID should not be None!"
    assert user.email is not None, "User email should not be None!"

    db_session.delete(user)
    db_session.commit()
    LOG.debug(f"Deleted user with ID: {user.id}")

    user = db_session.execute(
        select(User).filter(User.id == user.id)
    ).scalar_one_or_none()
    assert user is None, f"User with ID {user.id} should not be found in the database!"


def test_create_and_retrieve_multiple_users_success(db_session: Session):
    """
    Test successful creation and retrieval of multiple users.

    Requirements:
        - List of user data is provided.

    Steps:
        1. For each user data, create a user and persist in the database.
        2. For each known user data, retrieve a user by its email and assert its properties.

    Pass criteria:
        - All created users are successfully retrieved and their properties match the known data.
    """
    for user_data in const.SAMPLE_USER_DATA:
        user = add_user_to_db(db_session, user_data)

        retrieved_user = db_session.execute(
            select(User).filter(User.email == user_data["email"])
        ).scalar_one_or_none()
        assert retrieved_user is not None

    users = db_session.query(User).all()
    assert len(users) == len(const.SAMPLE_USER_DATA)
    for user in users:
        assert_user_properties(user, const.SAMPLE_USER_DATA[user.id - 1])


def test_add_user_with_the_same_email_fails(db_session: Session):
    """
    Test the attempt to add a user with an email that already exists in the database.

    Requirements:
        - A user is previously added to the database.
        - An attempt is made to add another user with the same email.

    Steps:
        1. Add a user to the database using the first sample data.
        2. Create another user instance with the same email (from the sample data).
        3. Try to add this user to the database and commit the changes.

    Pass criteria:
        The raised exception message contains "UNIQUE constraint failed: user.email".
    """
    user_data = const.SAMPLE_USER_DATA[0]
    user = add_user_to_db(db_session, user_data)
    assert user is not None

    user = User(**user_data)
    db_session.add(user)
    with pytest.raises(Exception) as excinfo:
        db_session.commit()
    assert "UNIQUE constraint failed: user.email" in str(excinfo.value)
