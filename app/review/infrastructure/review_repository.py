import json
from pathlib import Path
from uuid import UUID

from app.review.domain.review import Review


DATA_FILE = Path("data/reviews.json")


def review_to_dict(review: Review) -> dict:
    return {
        "id": str(review.id),
        "booking_id": str(review.booking_id),
        "customer_id": str(review.customer_id),
        "provider_id": str(review.provider_id),
        "service_id": str(review.service_id),
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at,
        "updated_at": review.updated_at
    }


def dict_to_review(data: dict) -> Review:
    return Review(
        id=UUID(data["id"]),
        booking_id=UUID(data["booking_id"]),
        customer_id=UUID(data["customer_id"]),
        provider_id=UUID(data["provider_id"]),
        service_id=UUID(data["service_id"]),
        rating=int(data["rating"]),
        comment=data["comment"],
        created_at=data["created_at"],
        updated_at=data["updated_at"]
    )


def load_reviews() -> list[Review]:
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text("[]")

    content = DATA_FILE.read_text().strip()

    if content == "":
        return []

    reviews_data = json.loads(content)

    return [dict_to_review(review_data) for review_data in reviews_data]


def save_reviews(reviews: list[Review]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    reviews_data = [review_to_dict(review) for review in reviews]

    DATA_FILE.write_text(json.dumps(reviews_data, indent=4))


def find_all() -> list[Review]:
    return load_reviews()


def find_by_booking_id(booking_id: UUID) -> Review | None:
    reviews = load_reviews()

    for review in reviews:
        if review.booking_id == booking_id:
            return review

    return None


def find_by_customer_id(customer_id: UUID) -> list[Review]:
    reviews = load_reviews()

    return [
        review
        for review in reviews
        if review.customer_id == customer_id
    ]


def find_by_provider_id(provider_id: UUID) -> list[Review]:
    reviews = load_reviews()

    return [
        review
        for review in reviews
        if review.provider_id == provider_id
    ]


def find_by_service_id(service_id: UUID) -> list[Review]:
    reviews = load_reviews()

    return [
        review
        for review in reviews
        if review.service_id == service_id
    ]


def save(review: Review) -> Review:
    reviews = load_reviews()
    reviews.append(review)
    save_reviews(reviews)

    return review