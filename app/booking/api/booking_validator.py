from datetime import datetime


def validate_create_booking_data(
    booking_date: str,
    booking_time: str,
    address: str
) -> list[str]:
    errors = []

    if not booking_date or booking_date.strip() == "":
        errors.append("Booking date is required")
    elif not is_valid_date(booking_date):
        errors.append("Booking date is invalid")

    if not booking_time or booking_time.strip() == "":
        errors.append("Booking time is required")
    elif not is_valid_time(booking_time):
        errors.append("Booking time is invalid")

    if not address or address.strip() == "":
        errors.append("Address is required")

    return errors


def is_valid_date(value: str) -> bool:
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_time(value: str) -> bool:
    try:
        datetime.strptime(value, "%H:%M")
        return True
    except ValueError:
        return False