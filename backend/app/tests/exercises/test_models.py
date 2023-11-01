import pytest
import logging
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from sqlalchemy.exc import IntegrityError

from app.models import Category, Exercise
from app.tests import const
from app.tests.utils import add_model_to_db


LOG = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "create_category_model", const.SAMPLE_CATEGORY_DATA[:1], indirect=True
)
def test_create_category_success(create_category_model: tuple[Category, dict]):
    """
    Test creating a category with valid data success.

    Requirements:
        - Database session available.

    Steps:
        1. Create a category with valid data.
        2. Verify the category was added to the database.

    Pass criteria:
        - The category was added to the database.
        - The category data matches the expected data.
    """
    category, expected = create_category_model
    assert (
        category.name == expected["name"]
    ), f"Actual name \"{category.name}\" does not match with expected \"{expected['name']}\""
    assert category.id is not None, "Category ID should not be None!"
    assert isinstance(
        category.exercises, list
    ), f"Category exercises should be a list instead of {type(category.exercises)}!"
    assert (
        len(category.exercises) == 0
    ), f"Category exercises should be empty instead of {category.exercises}!"


@pytest.mark.parametrize(
    "create_category_model", const.SAMPLE_CATEGORY_DATA[:1], indirect=True
)
def test_create_category_duplicate_name_fails(
    create_category_model: tuple[Category, dict], db_session: Session
):
    """
    Test creating a category with duplicate name raises IntegrityError.

    Requirements:
        - Database session available.

    Steps:
        1. Create a category with sample data.
        2. Attempt to add the same category data to the database.
        3. Verify that an IntegrityError is raised.

    Pass criteria:
        - An IntegrityError is raised when attempting to add a category with duplicate name.
    """
    _, category_data = create_category_model
    with pytest.raises(IntegrityError):
        add_model_to_db(db_session, Category, category_data)


def test_multiple_categories(db_session: Session):
    """
    Test creating multiple categories.

    Requirements:
        - Database session available.

    Steps:
        1. Create multiple categories with sample data.
        2. Verify the categories were added to the database.

    Pass criteria:
        - The categories were added to the database.
        - The categories data matches the expected data.
    """
    for category_data in const.SAMPLE_CATEGORY_DATA:
        add_model_to_db(db_session, Category, category_data)

        retrieved_category = db_session.execute(
            select(Category).filter(Category.name == category_data["name"])
        ).scalar_one_or_none()
        assert (
            retrieved_category is not None
        ), f"Category with name \"{category_data['name']}\" should not be None!"
        assert (
            retrieved_category.name == category_data["name"]
        ), f"Actual name \"{retrieved_category.name}\" does not match with expected \"{category_data['name']}\""

    categories = db_session.scalars(select(Category)).all()
    LOG.debug(f"Retrieved categories: {categories}")
    assert len(categories) == len(
        const.SAMPLE_CATEGORY_DATA
    ), f'Actual number of categories "{len(categories)}" does not match with expected "{len(const.SAMPLE_CATEGORY_DATA)}"'


@pytest.mark.parametrize(
    "create_category_model", const.SAMPLE_CATEGORY_DATA[:1], indirect=True
)
def test_update_category_success(
    create_category_model: tuple[Category, dict], db_session: Session
):
    """
    Test updating a category with valid data success.

    Requirements:
        - Database session available.

    Steps:
        1. Add sample category data to the database.
        2. Retrieve a category from the database.
        3. Update the category with sample data.
        4. Verify the category was updated in the database.

    Pass criteria:
        - The category was updated in the database.
        - The category data matches the expected data.
    """
    category, _ = create_category_model
    assert category is not None, "Category has not been added to database!"
    updated_name = "new test name"
    LOG.debug(f'Updating category: {category} with name "{updated_name}"')
    category.name = updated_name
    db_session.commit()
    category = db_session.execute(
        select(Category).filter(Category.id == category.id)
    ).scalar_one()
    LOG.debug(f"Retrieved category: {category}")
    assert category is not None, "Category has not been added to database!"
    assert (
        category.name == updated_name
    ), f'Actual name "{category.name}" does not match with expected "{updated_name}"'
    assert (
        category.id == 1
    ), f'Actual ID "{category.id}" does not match with expected "1"'


def test_update_category_with_existing_name_fails(db_session: Session):
    """
    Test that updating a category with an existing name fails due to a unique constraint violation.

    Requirements:
        - Database session available.

    Steps:
        1. Add sample category data to the database.
        2. Retrieve a category from the database.
        3. Update the category with an existing name.
        4. Attempt to commit the changes to the database.
        5. Verify that an IntegrityError is raised.

    Pass criteria:
        - An IntegrityError is raised when attempting to update a category with an existing name.
    """
    for category in const.SAMPLE_CATEGORY_DATA:
        add_model_to_db(db_session, Category, category)
    category = db_session.execute(
        select(Category).filter(Category.id == 1)
    ).scalar_one()
    LOG.debug(f"Retrieved category: {category}")
    existing_name = const.SAMPLE_CATEGORY_DATA[-1]["name"]
    LOG.debug(f'Updating category: {category} with name "{existing_name}"')
    category.name = existing_name
    with pytest.raises(IntegrityError):
        db_session.commit()


@pytest.mark.parametrize(
    "create_category_model", const.SAMPLE_CATEGORY_DATA[:1], indirect=True
)
def test_delete_category_success(
    create_category_model: tuple[Category, dict], db_session: Session
):
    """
    Test that deleting a category from the database is successful.

    Requirements:
        - Database session available.

    Steps:
        1. Create a sample category model.
        2. Delete the category from the database.
        3. Verify that the category has been deleted from the database.

    Pass criteria:
        - The category is deleted from the database.
    """
    category, _ = create_category_model
    assert category is not None, "Category has not been added to database!"
    db_session.delete(category)
    db_session.commit()
    category = db_session.execute(
        select(Category).filter(Category.id == category.id)
    ).scalar_one_or_none()
    assert category is None, "Category has not been deleted from database!"


@pytest.mark.parametrize(
    "create_category_model", const.SAMPLE_CATEGORY_DATA[:1], indirect=True
)
def test_create_exercise_success(
    create_category_model: tuple[Category, dict], db_session: Session
):
    """
    Test creating an exercise with valid data success.

    Requirements:
        - Database session available.
        - Category is previously created in the database.

    Steps:
        1. Create a category with sample data.
        2. Create an exercise with sample data.
        3. Verify the exercise was added to the database.

    Pass criteria:
        - The exercise was added to the database.
        - The exercise data matches the expected data.
        - The exercise category matches the expected category.
    """
    _, category_data = create_category_model
    exercise_data = const.SAMPLE_EXERCISE_DATA[0]
    exercise = add_model_to_db(db_session, Exercise, exercise_data)
    assert (
        exercise.name == exercise_data["name"]
    ), f"Actual name \"{exercise.name}\" does not match with expected \"{exercise_data['name']}\""
    assert (
        exercise.description == exercise_data["description"]
    ), f"Actual description \"{exercise.description}\" does not match with expected \"{exercise_data['description']}\""
    assert (
        exercise.category_id == 1
    ), f'Actual category ID "{exercise.category_id}" does not match with expected "1"'
    assert (
        exercise.category.name == category_data["name"]
    ), f"Actual category \"{exercise.category.name}\" does not match with expected \"{category_data['name']}\""
