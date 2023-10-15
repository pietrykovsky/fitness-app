# Import all the models, so that Base has them before being
# imported by Alembic
from app.core.database import Base
from app.models import Item, User
