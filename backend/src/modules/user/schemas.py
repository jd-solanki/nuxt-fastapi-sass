from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.modules.helpers.schemas import EntityInsertMeta


# 👉 Base Models
class UserBase(BaseModel):
    username: str = Field(max_length=30)
    email: EmailStr = Field(max_length=254)


class UserBasePartial(BaseModel):
    username: str | None = Field(max_length=30, default=None)
    email: EmailStr | None = Field(max_length=254, default=None)


# 👉 CRUD models
class UserCreate(UserBase):
    password: str


class UserRead(UserBase, EntityInsertMeta):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserUpdate(UserBasePartial):
    password: str | None = None
