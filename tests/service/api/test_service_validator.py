from app.service.api.service_validator import validate_create_service_data


def test_create_service_validation_requires_main_fields():
    errors = validate_create_service_data(
        name="",
        description="",
        category="",
        price="",
        duration_minutes="",
        image=object()
    )

    assert "Service name is required" in errors
    assert "Service description is required" in errors
    assert "Service category is required" in errors
    assert "Service price is required" in errors
    assert "Service duration is required" in errors


def test_create_service_validation_rejects_invalid_price():
    errors = validate_create_service_data(
        name="Home Cleaning",
        description="General home cleaning service",
        category="Cleaning",
        price="wrong-price",
        duration_minutes="60",  
        image=object()
    )

    assert "Service price must be a positive number" in errors


def test_create_service_validation_rejects_invalid_duration():
    errors = validate_create_service_data(
        name="Home Cleaning",
        description="General home cleaning service",
        category="Cleaning",
        price="250",
        duration_minutes="wrong-duration",
        image=object()
    )

    assert "Service duration must be a positive number" in errors


def test_create_service_validation_accepts_valid_data():
    errors = validate_create_service_data(
        name="Home Cleaning",
        description="General home cleaning service",
        category="Cleaning",
        price="250",
        duration_minutes="60",
        image=object()
    )

    assert errors == []