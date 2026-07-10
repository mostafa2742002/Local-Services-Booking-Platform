from datetime import datetime
from uuid import uuid4

from werkzeug.security import generate_password_hash, check_password_hash

from app.user.domain.user import User
from app.user.domain.role import Role
from app.user.infrastructure.user_repository import find_by_email, save


def register_user(name: str, email: str, password: str, role: Role = Role.CUSTOMER) -> User:
    existing_user = find_by_email(email)

    if existing_user is not None:
        raise ValueError("Email already exists")

    now = datetime.now().isoformat(timespec="seconds")

    user = User(
        id=uuid4(),
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
        created_at=now,
        updated_at=now
    )

    return save(user)


def login_user(email: str, password: str) -> User:
    user = find_by_email(email)

    if user is None:
        raise ValueError("Invalid email or password")

    is_password_correct = check_password_hash(user.password_hash, password)

    if not is_password_correct:
        raise ValueError("Invalid email or password")

    return user