from datetime import datetime

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    first_name: str
    last_name: str
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None


class UserInDB(UserBase):
    id: int | None = None
    create_date: datetime | None = None

    class ConfigDict:
        from_attributes = True
