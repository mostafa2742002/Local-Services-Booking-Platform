def validate_create_review_data(rating: str) -> list[str]:
    errors = []

    if not rating or rating.strip() == "":
        errors.append("Rating is required")
    elif not is_valid_rating(rating):
        errors.append("Rating must be between 1 and 5")

    return errors


def is_valid_rating(value: str) -> bool:
    try:
        rating = int(value)
        return 1 <= rating <= 5
    except ValueError:
        return False