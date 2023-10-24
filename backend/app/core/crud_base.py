from typing import Any

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import Base


type ModelType = Base
type CreateSchemaType = BaseModel
type UpdateSchemaType = BaseModel


class CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]:
    """
    Base class for CRUD operations with SQLAlchemy models.

    :param model: SQLAlchemy model to perform CRUD operations on.
    """

    def __init__(self, model: ModelType):
        self.model = model

    def get(self, db: Session, **kwargs) -> ModelType | None:
        """
        Retrieve a single record from the database by filtering with the given keyword arguments.

        :param db: SQLAlchemy database session.
        :param kwargs: Keyword arguments to filter the record.
        :return: Retrieved record or None if not found.
        """
        return db.query(self.model).filter_by(**kwargs).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        """
        Retrieve multiple records from the database with optional pagination.

        :param db: SQLAlchemy database session.
        :param skip: Number of records to skip.
        :param limit: Maximum number of records to retrieve.
        :return: List of retrieved records.
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record in the database.

        :param db: SQLAlchemy database session.
        :param obj_in: Pydantic model representing the record to create.
        :return: Created record.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        """
        Update an existing record in the database.

        :param db: SQLAlchemy database session.
        :param db_obj: Record to update.
        :param obj_in: Pydantic model or dictionary representing the updated values.
        :return: Updated record.
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, **kwargs) -> ModelType:
        """
        Delete a record from the database by ID or other attributes.

        :param db: SQLAlchemy database session.
        :param kwargs: Keyword arguments representing attributes of the record to delete.
        :return: The deleted record.
        """
        obj = self.get(db, **kwargs)
        db.delete(obj)
        db.commit()
        return obj
