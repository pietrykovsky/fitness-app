import logging
import pytest
from sqlalchemy.orm import Session

from app.models import Category
from app.tests.utils import add_model_to_db


LOG = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def create_category_model(
    request: pytest.FixtureRequest, db_session: Session
) -> tuple[Category, dict]:
    """
    Create a category fixture in the database.

    :param category: The category data to use for creating the category.
    :param db_session: The database session to use for adding the category.
    :return: The added category instance.
    """
    LOG.debug(f"Creating category with data: {request.param}")
    instance = add_model_to_db(db_session, Category, request.param)
    LOG.debug(f"Added category to database: {instance}")
    return instance, request.param
