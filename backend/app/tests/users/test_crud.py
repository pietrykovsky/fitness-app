import pytest
import logging
from sqlalchemy.orm import Session

from app.crud import user as user_crud
from app.models import User
from app.schemas import UserCreate
from app.tests import const
from app.tests.utils import assert_user_properties, add_user_to_db
from app.core.security import verify_password


LOG = logging.getLogger(__name__)


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
def test_get_user_by_id(create_user_model: tuple[User, dict], db_session: Session):
    """
    Test retrieving a user by its ID.

    Requirements:
        - User is previously created in the database.

    Steps:
        1. Retrieve a user by its known ID.
        2. Assert properties of the retrieved user against the known data.

    Pass criteria:
        - User properties match the known data.
    """
    user, expected = create_user_model
    retrieved_user = user_crud.get(db_session, id=user.id)
    LOG.debug(f"Retrieved user: id={retrieved_user.id}, email={retrieved_user.email}")
    assert_user_properties(retrieved_user, expected)


def test_create_user(db_session: Session):
    """
    Test creating a new user.

    Requirements:
        - User data is provided.

    Steps:
        1. Create a new user with the provided data.
        2. Assert properties of the user against the provided data.

    Pass criteria:
        - User properties match the provided data.
    """
    user_data = const.SAMPLE_USER_DATA[0]
    user = user_crud.create(db_session, obj_in=UserCreate(**user_data))
    LOG.debug(f"Created user with data: {user_data}")

    assert (
        user.email == user_data["email"]
    ), f"Actual email \"{user.email}\" does not match expected \"{user_data['email']}\""
    assert (
        user.first_name == user_data["first_name"]
    ), f"Actual first name \"{user.first_name}\" does not match expected \"{user_data['first_name']}\""
    assert (
        user.last_name == user_data["last_name"]
    ), f"Actual last name \"{user.last_name}\" does not match expected \"{user_data['last_name']}\""
    assert verify_password(
        user_data["password"], user.password
    ), f"Could not verified password \"{user_data['password']}\""
    assert user.is_superuser is False, "User should not be a superuser by default!"
    assert user.is_active is True, "User should be active by default!"


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
def test_update_user(create_user_model: tuple[User, dict], db_session: Session):
    """
    Test updating a user's properties.

    Requirements:
        - User is previously created in the database.

    Steps:
        1. Update known properties of the user.
        2. Persist the changes to the database.
        3. Assert updated properties of the user.

    Pass criteria:
        - Updated user properties match the new data.
    """
    NEW_EMAIL = "new_email@example.com"
    NEW_FIRST_NAME = "new_first_name"

    user, _ = create_user_model
    update_data = {"email": NEW_EMAIL, "first_name": NEW_FIRST_NAME}
    updated_user = user_crud.update(db_session, db_obj=user, obj_in=update_data)
    LOG.debug(f"Updated user with data: {update_data}")

    assert (
        updated_user.email == NEW_EMAIL
    ), f'Actual email "{updated_user.email}" does not match expected "{NEW_EMAIL}"'
    assert (
        updated_user.first_name == NEW_FIRST_NAME
    ), f'Actual first name "{updated_user.first_name}" does not match expected "{NEW_FIRST_NAME}"'


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
def test_delete_user(create_user_model: tuple[User, dict], db_session: Session):
    """
    Test deleting a user.

    Requirements:
        - User is previously created in the database.

    Steps:
        1. Delete the user.
        2. Try to retrieve the user by its ID.

    Pass criteria:
        - User is not found in the database.
    """
    user, _ = create_user_model
    user_crud.remove(db_session, id=user.id)
    LOG.debug(f"Deleted user with ID: {user.id}")
    user_after_delete = user_crud.get(db_session, id=user.id)
    assert (
        user_after_delete is None
    ), f"User with ID {user.id} should not be found in the database!"


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA[:1], indirect=True)
def test_get_user_by_email(create_user_model: tuple[User, dict], db_session: Session):
    """
    Test retrieving a user by its email.

    Requirements:
        - User is previously created in the database.

    Steps:
        1. Retrieve a user by its known email.
        2. Assert properties of the retrieved user against the known data.

    Pass criteria:
        - User properties match the known data.
    """
    _, expected = create_user_model
    retrieved_user = user_crud.get(db_session, email=expected["email"])
    LOG.debug(f"Retrieved user: id={retrieved_user.id}, email={retrieved_user.email}")
    assert_user_properties(retrieved_user, expected)


def test_authenticate_user(db_session: Session):
    """
    Test authenticating a user.

    Requirements:
        - User is previously created in the database.

    Steps:
        1. Authenticate the user with the known email and password.
        2. Assert properties of the authenticated user against the known data.

    Pass criteria:
        - User properties match the known data.
    """
    expected = const.SAMPLE_USER_DATA[0]
    user_crud.create(db_session, obj_in=UserCreate(**expected))
    LOG.debug(f"Created user with data: {expected}")
    user = user_crud.authenticate(
        db_session, email=expected["email"], password=expected["password"]
    )
    assert user is not None, f"User not found in database: {expected}"
    assert (
        user.email == expected["email"]
    ), f"Actual email \"{user.email}\" does not match expected \"{expected['email']}\""


def test_get_all_users(db_session: Session):
    """
    Test retrieving all users.

    Requirements:
        - Users are previously created in the database.

    Steps:
        1. Create users in the database.
        2. Retrieve all users.
        3. Assert the number of retrieved users.

    Pass criteria:
        - Number of retrieved users matches the number of created users.
    """
    for user_data in const.SAMPLE_USER_DATA:
        add_user_to_db(db_session, user_data)
    users = user_crud.get_multi(db_session)
    LOG.debug(f"Retrieved {len(users)} users from database.")
    LOG.debug(f"Users: {users}")
    assert len(users) == len(
        const.SAMPLE_USER_DATA
    ), f"Actual number of users {len(users)} does not match expected {len(const.SAMPLE_USER_DATA)}"
