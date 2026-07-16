from app.booking.api.booking_validator import validate_create_booking_data


def test_create_booking_validation_requires_main_fields():
    errors = validate_create_booking_data(
        booking_date="",
        booking_time="",
        address="",
        phone_number=""
    )

    assert "Booking date is required" in errors
    assert "Booking time is required" in errors
    assert "Address is required" in errors
    assert "Phone number is required" in errors


def test_create_booking_validation_rejects_invalid_date():
    errors = validate_create_booking_data(
        booking_date="wrong-date",
        booking_time="10:30",
        address="Cairo",
        phone_number="01012345678"
    )

    assert "Booking date is invalid" in errors


def test_create_booking_validation_rejects_invalid_time():
    errors = validate_create_booking_data(
        booking_date="2026-01-01",
        booking_time="wrong-time",
        address="Cairo",
        phone_number="01012345678"
    )

    assert "Booking time is invalid" in errors


def test_create_booking_validation_accepts_valid_data():
    errors = validate_create_booking_data(
        booking_date="2026-01-01",
        booking_time="10:30",
        address="Cairo",
        phone_number="01012345678"
    )

    assert errors == []