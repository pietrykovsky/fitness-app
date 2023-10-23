from sqlalchemy.orm import Session

from app import models, schemas
from app.core.crud_base import CRUDBase


class CRUDItem(CRUDBase[models.Item, schemas.ItemCreate, schemas.Item]):
    def create(
        self, db: Session, *, item: schemas.ItemCreate, user_id: int
    ) -> models.Item:
        db_item = models.Item(**item.dict(), owner_id=user_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item


item = CRUDItem(models.Item)
user = CRUDBase[models.User, schemas.UserCreate, schemas.User](models.User)
