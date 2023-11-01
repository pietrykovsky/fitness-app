from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey

from app.core.database import Base


class Category(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    exercises: Mapped[list["Exercise"]] = relationship(
        "Exercise", back_populates="category"
    )

    def __repr__(self) -> str:
        return f"<Category: {self.name}>"


class Exercise(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship(back_populates="exercises")

    def __repr__(self) -> str:
        return f"<Exercise: {self.name}>"
