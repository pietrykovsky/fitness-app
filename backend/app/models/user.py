from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[str] = mapped_column(index=True)
    last_name: Mapped[str] = mapped_column(index=True)
    password: Mapped[str]
    is_active: Mapped[bool] = True
    is_superuser: Mapped[bool] = False
    create_date: Mapped[datetime] = mapped_column(server_default=func.now())
