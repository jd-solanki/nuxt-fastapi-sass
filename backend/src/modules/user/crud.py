from datetime import datetime, timedelta
from typing import Any

import bcrypt
from fastapi import HTTPException, status
from sqlalchemy import exc
from sqlalchemy.orm import Session

from src.modules.helpers import hash

from . import models, schemas


# ℹ️ return type of hashpw is bytes
def hash_pwd(pwd: str) -> bytes:
    return bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())


# 👉 Create
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_pwd = str(hash_pwd(user.password))

    db_user = models.User(
        username=user.username, email=user.email, hashed_pwd=hashed_pwd
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# 👉 Read
# TODO: Add pagination
def get_users(db: Session) -> list[models.User]:
    return db.query(models.User).all()


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).get(user_id)


def get_user_by_username(db: Session, username: str) -> models.User | None:
    partial_query = db.query(models.User).where(models.User.username == username)
    try:
        return partial_query.one_or_none()
    except exc.MultipleResultsFound:
        print("Report admins about there is multiple records with same username")
        return partial_query.first()


def get_user_or_404(
    db: Session,
    user_id: int,
    err_404_msg: str = "User you want to get doesn't exist",
) -> models.User:
    db_user = get_user(db, user_id)

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err_404_msg)

    return db_user


# 👉 Update
def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = get_user_or_404(db, user_id, "User you want to update doesn't exist")

    # `if value else None` skip assigning optional fields forcefully to `None`
    for property, value in vars(user).items():
        setattr(db_user, property, value) if value else None

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# 👉 Delete
def delete_user(db: Session, user_id: int):
    db_user = get_user_or_404(db, user_id, "User you want to delete doesn't exist")

    db.delete(db_user)
    db.commit()


# 👉 Token
def create_access_token(data: dict[Any, Any], expires_delta: timedelta | None = None):
    # Copy passed data
    to_encode = data.copy()

    # Calculate expire time by adding expires_delta to current UTC time
    # If expires_delta is provided use it or use 15 minutes as default for adding in current UTC time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    # add `exp` key to data dict that represents the expiration time of JWT
    to_encode.update({"exp": expire})

    # Return encoded JWT
    return hash.encode_jwt(to_encode)
