import bcrypt
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
