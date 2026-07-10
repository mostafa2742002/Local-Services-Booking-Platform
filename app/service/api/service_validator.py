def validate_create_service_data(
    name: str,
    description: str,
    category: str,
    price: str,
    duration_minutes: str
) -> list[str]:
    errors = []

    if not name or name.strip() == "":
        errors.append("Service name is required")

    if not description or description.strip() == "":
        errors.append("Service description is required")

    if not category or category.strip() == "":
        errors.append("Service category is required")

    if not price or price.strip() == "":
        errors.append("Service price is required")
    elif not is_positive_float(price):
        errors.append("Service price must be a positive number")

    if not duration_minutes or duration_minutes.strip() == "":
        errors.append("Service duration is required")
    elif not is_positive_integer(duration_minutes):
        errors.append("Service duration must be a positive number")

    return errors


def is_positive_float(value: str) -> bool:
    try:
        number = float(value)
        return number > 0
    except ValueError:
        return False


def is_positive_integer(value: str) -> bool:
    try:
        number = int(value)
        return number > 0
    except ValueError:
        return False