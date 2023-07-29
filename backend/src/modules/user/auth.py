from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.modules.helpers import hash

from . import crud, models

ACCESS_TOKEN_EXPIRES_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def authenticate_user(
    db: Session, username: str, password: str
) -> Optional[models.User]:
    """
    Authenticates a user by checking if the provided username and password match a user in the database.

    Args:
        db (Session): The database session.
        username (str): The username of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        Optional[models.User]: The authenticated user if the provided username and password match a user in the database,
        otherwise None.

    Example:
        >>> from sqlalchemy.orm import Session
        >>> from src.modules.user import auth
        >>> from src.modules.user.models import User
        >>> from src.modules.helpers.hash import hash_password
        >>> from src.modules.user.crud import create_user
        >>> from src.db.base import Base, engine
        >>> Base.metadata.create_all(bind=engine)
        >>> db = Session(bind=engine)
        >>> user = User(username="testuser", hashed_pwd=hash_password("testpassword"))
        >>> create_user(db, user)
        >>> authenticated_user = auth.authenticate_user(db, "testuser", "testpassword")
        >>> authenticated_user.username
        'testuser'
    """
    user = crud.get_user_by_username(db, username)

    if not user:
        return None

    if not hash.verify_password(password, user.hashed_pwd):
        return None

    return user
