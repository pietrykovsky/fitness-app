from app.core.crud_base import CRUDBase
from app.models import Category
from app.schemas import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass


category = CRUDCategory(Category)
