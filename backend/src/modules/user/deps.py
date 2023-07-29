from typing import Annotated, cast

from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session

from src.modules.helpers import hash

from . import auth, crud, models


async def get_current_user(
    db: Session, token: Annotated[str, Depends(auth.oauth2_scheme)]
) -> models.User:
    """
    Get the current user from the database based on the JWT token.

    Args:
        db (Session): The SQLAlchemy database session.
        token (str): The JWT token passed in the Authorization header.

    Raises:
        HTTPException: If the credentials cannot be validated.

    Returns:
        User: The user object for the authenticated user.

    Example:
        To get the current user, you can use the following code:

        >>> from sqlalchemy.orm import Session
        >>> from src.modules.user import auth, deps
        >>> from src.modules.user.models import User
        >>> db = Session()
        >>> token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        >>> user = await deps.get_current_user(db=db, token=token)
        >>> print(user.username)
        "john_doe"
    """

    # Store HTTP exception for later usage
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    # Try to decode the JWT
    try:
        payload = hash.decode_jwt(token)

        # Get username from payload via "sub" property
        # What is "sub"? => https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#technical-details-about-the-jwt-subject-sub
        username = cast(str | None, payload.get("sub"))

        # If we can't find username raise defined `credential_exception`
        if username is None:
            raise credential_exception

    # Raise `credential_exception` if there's exception is raised while decoding JWT
    except JWTError:
        raise credential_exception

    # Get user by username
    user = crud.get_user_by_username(db=db, username=username)

    # If there's no username by username we get from token raise `credential_exception`
    if user is None:
        raise credential_exception

    # Finally, If everything is fine, return user we get from DB
    return user


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
) -> models.User:
    """
    Return current active user using `get_current_user` dependency. If user is not active user, it raise exception.

    Args:
        current_user (User): The user object for the authenticated user.

    Raises:
        HTTPException: If the user is not active.

    Returns:
        User: The active user object for the authenticated user.

    Example:
        To get the current active user, you can use the following code:

        >>> from sqlalchemy.orm import Session
        >>> from src.modules.user import auth, deps
        >>> from src.modules.user.models import User
        >>> db = Session()
        >>> token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        >>> user = await deps.get_current_user(db=db, token=token)
        >>> active_user = await deps.get_current_active_user(current_user=user)
        >>> print(active_user.username)
        "john_doe"
    """
    # If requested user, we get from fastAPI dependency isn't active user raise exception
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    # As user is active, return it
    return current_user
