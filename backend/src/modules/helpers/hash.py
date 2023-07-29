from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "cd0fb7dad8e13d40b3ca8f5466f4694a037cf99854e152c37e3a2770a966a6bb"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str | bytes, hashed_password: str | bytes):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def encode_jwt(data: Any):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
