import re


def validate_register_data(name: str, email: str, password: str, confirm_password: str) -> list[str]:
    errors = []

    if not name or name.strip() == "":
        errors.append("Name is required")

    if not email or email.strip() == "":
        errors.append("Email is required")
    elif not is_valid_email(email):
        errors.append("Email is invalid")

    if not password or password.strip() == "":
        errors.append("Password is required")
    elif len(password) < 6:
        errors.append("Password must be at least 6 characters")

    if password != confirm_password:
        errors.append("Passwords do not match")

    return errors


def validate_login_data(email: str, password: str) -> list[str]:
    errors = []

    if not email or email.strip() == "":
        errors.append("Email is required")
    elif not is_valid_email(email):
        errors.append("Email is invalid")

    if not password or password.strip() == "":
        errors.append("Password is required")

    return errors


def is_valid_email(email: str) -> bool:
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(email_pattern, email) is not None