from datetime import datetime


def validate_create_booking_data(
    booking_date: str,
    booking_time: str,
    address: str,
    phone_number: str
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
    elif not is_time_in_future(booking_date, booking_time):
        errors.append("Booking time cannot be in the past")

    if not address or address.strip() == "":
        errors.append("Address is required")

    if not phone_number or phone_number.strip() == "":
        errors.append("Phone number is required")
        
    if is_valid_phone_number(phone_number) is False:
        errors.append("Phone number is invalid")
    

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
    
def is_valid_phone_number(value: str) -> bool:
    if not value.isdigit():
        return False
    if len(value) < 10:
        return False
    if not (value.startswith("010") or value.startswith("011") or value.startswith("012") or value.startswith("015")):
        return False

    return True

def is_time_in_future(booking_date: str, booking_time: str) -> bool:
    try:
        booking_datetime = datetime.strptime(f"{booking_date} {booking_time}", "%Y-%m-%d %H:%M")
        return booking_datetime > datetime.now()
    except ValueError:
        return False