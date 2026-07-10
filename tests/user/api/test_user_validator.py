from app.user.api.user_validator import validate_register_data, validate_login_data


def test_register_validation_requires_name_email_and_password():
    errors = validate_register_data("", "", "", "")

    assert "Name is required" in errors
    assert "Email is required" in errors
    assert "Password is required" in errors


def test_register_validation_rejects_invalid_email():
    errors = validate_register_data(
        name="Test User",
        email="invalid-email",
        password="123456",
        confirm_password="123456"
    )

    assert "Email is invalid" in errors


def test_register_validation_rejects_short_password():
    errors = validate_register_data(
        name="Test User",
        email="test@example.com",
        password="123",
        confirm_password="123"
    )

    assert "Password must be at least 6 characters" in errors


def test_register_validation_rejects_password_mismatch():
    errors = validate_register_data(
        name="Test User",
        email="test@example.com",
        password="123456",
        confirm_password="abcdef"
    )

    assert "Passwords do not match" in errors


def test_register_validation_accepts_valid_data():
    errors = validate_register_data(
        name="Test User",
        email="test@example.com",
        password="123456",
        confirm_password="123456"
    )

    assert errors == []


def test_login_validation_requires_email_and_password():
    errors = validate_login_data("", "")

    assert "Email is required" in errors
    assert "Password is required" in errors


def test_login_validation_rejects_invalid_email():
    errors = validate_login_data("invalid-email", "123456")

    assert "Email is invalid" in errors


def test_login_validation_accepts_valid_data():
    errors = validate_login_data("test@example.com", "123456")

    assert errors == []