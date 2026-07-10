import pytest
from uuid import uuid4

from werkzeug.security import generate_password_hash, check_password_hash

from app.user.application import user_service
from app.user.domain.user import User
from app.user.domain.role import Role

def test_register_user_creates_user_with_hashed_password(monkeypatch):
    saved_users = []

    def fake_find_by_email(email):
        return None

    def fake_save(user):
        saved_users.append(user)
        return user

    monkeypatch.setattr(user_service, "find_by_email", fake_find_by_email)
    monkeypatch.setattr(user_service, "save", fake_save)

    user = user_service.register_user(
        name="Test User",
        email="test@example.com",
        password="123456"
    )

    assert user.name == "Test User"
    assert user.email == "test@example.com"
    assert user.role == Role.CUSTOMER
    assert user.password_hash != "123456"
    assert check_password_hash(user.password_hash, "123456")
    assert len(saved_users) == 1


def test_register_user_rejects_duplicate_email(monkeypatch):
    existing_user = User(
        id=uuid4(),
        name="Existing User",
        email="test@example.com",
        password_hash="hashed-password",
        role=Role.CUSTOMER,
        created_at="2026-01-01T10:00:00",
        updated_at="2026-01-01T10:00:00"
    )

    def fake_find_by_email(email):
        return existing_user

    monkeypatch.setattr(user_service, "find_by_email", fake_find_by_email)

    with pytest.raises(ValueError, match="Email already exists"):
        user_service.register_user(
            name="Test User",
            email="test@example.com",
            password="123456"
        )
    


def test_login_user_returns_user_when_credentials_are_valid(monkeypatch):
    existing_user = User(
        id=uuid4(),
        name="Test User",
        email="test@example.com",
        password_hash=generate_password_hash("123456"),
        role=Role.CUSTOMER,
        created_at="2026-01-01T10:00:00",
        updated_at="2026-01-01T10:00:00"
    )

    def fake_find_by_email(email):
        return existing_user

    monkeypatch.setattr(user_service, "find_by_email", fake_find_by_email)

    logged_in_user = user_service.login_user(
        email="test@example.com",
        password="123456"
    )

    assert logged_in_user == existing_user


def test_login_user_rejects_unknown_email(monkeypatch):
    def fake_find_by_email(email):
        return None

    monkeypatch.setattr(user_service, "find_by_email", fake_find_by_email)

    with pytest.raises(ValueError, match="Invalid email or password"):
        user_service.login_user(
            email="wrong@example.com",
            password="123456"
        )


def test_login_user_rejects_wrong_password(monkeypatch):
    existing_user = User(
        id=uuid4(),
        name="Test User",
        email="test@example.com",
        password_hash=generate_password_hash("123456"),
        role=Role.CUSTOMER,
        created_at="2026-01-01T10:00:00",
        updated_at="2026-01-01T10:00:00"
    )

    def fake_find_by_email(email):
        return existing_user

    monkeypatch.setattr(user_service, "find_by_email", fake_find_by_email)

    with pytest.raises(ValueError, match="Invalid email or password"):
        user_service.login_user(
            email="test@example.com",
            password="wrong-password"
        )