from typing import Tuple

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = 'HS256'


def verify_and_update(plain_password: str, hashed_password: str) -> Tuple[bool, str]:
    return pwd_context.verify_and_update(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
