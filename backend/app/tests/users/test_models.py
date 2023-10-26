import pytest

from app.models import User
from app.tests import const


@pytest.fixture(scope="function")
def create_user_model(request, db_session):
    user = User(**request.param)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user, request.param


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA, indirect=True)
def test_create_user_success(create_user_model):
    user, expected = create_user_model
    assert user.id is not None
    assert user.email == expected["email"]
    assert user.first_name == expected["first_name"]
    assert user.last_name == expected["last_name"]
    assert user.password == expected["password"]
    assert user.is_superuser is False
    assert user.is_active is True
    assert user.create_date is not None


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA, indirect=True)
def test_get_user_success(create_user_model, db_session):
    user, expected = create_user_model
    assert user is not None

    user = db_session.query(User).filter(User.id == user.id).first()
    assert user is not None
    assert user.id is not None
    assert user.email == expected["email"]
    assert user.first_name == expected["first_name"]
    assert user.last_name == expected["last_name"]
    assert user.password == expected["password"]
    assert user.is_superuser is False
    assert user.is_active is True
    assert user.create_date is not None


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA, indirect=True)
def test_update_user_success(create_user_model, db_session):
    new_password = "new_password"

    user, expected = create_user_model
    assert user is not None
    assert user.password == expected["password"]

    user.password = new_password
    db_session.commit()
    db_session.refresh(user)

    assert user.password == new_password


@pytest.mark.parametrize("create_user_model", const.SAMPLE_USER_DATA, indirect=True)
def test_delete_user_success(create_user_model, db_session):
    user, _ = create_user_model
    assert user.id is not None
    assert user.email is not None

    db_session.delete(user)
    db_session.commit()

    user = db_session.query(User).filter(User.id == user.id).first()
    assert user is None
