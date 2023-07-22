import bcrypt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

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
