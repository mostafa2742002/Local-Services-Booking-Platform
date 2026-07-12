from app.review.api.review_validator import validate_create_review_data


def test_create_review_validation_requires_rating():
    errors = validate_create_review_data("")

    assert "Rating is required" in errors


def test_create_review_validation_rejects_rating_less_than_one():
    errors = validate_create_review_data("0")

    assert "Rating must be between 1 and 5" in errors


def test_create_review_validation_rejects_rating_greater_than_five():
    errors = validate_create_review_data("6")

    assert "Rating must be between 1 and 5" in errors


def test_create_review_validation_rejects_non_number_rating():
    errors = validate_create_review_data("wrong-rating")

    assert "Rating must be between 1 and 5" in errors


def test_create_review_validation_accepts_valid_rating():
    errors = validate_create_review_data("5")

    assert errors == []