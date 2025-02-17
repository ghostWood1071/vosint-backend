from typing import Tuple

from passlib import pwd
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_and_update(
    plain_password: str, hashed_password: str
) -> Tuple[bool, str | None]:
    return pwd_context.verify_and_update(plain_password, hashed_password)


def verify_password_hash(password: str, hash: str) -> bool:
    return pwd_context.verify(password, hash)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def generate() -> str:
    return pwd.genword()
