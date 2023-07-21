from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str | None = Field(max_length=30)
    email: EmailStr | None = Field(max_length=254)
    # hashed_password: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int


class UserUpdate(UserBase):
    username: str = Field(max_length=30, default=None)
    email: EmailStr = Field(max_length=254)
    password: str | None = None
