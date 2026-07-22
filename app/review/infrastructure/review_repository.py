import json
from pathlib import Path
from uuid import UUID

from app.review.domain.review import Review


DATA_FILE = Path("data/reviews.json")

# function to convert a Review object to a dictionary for JSON serialization
def review_to_dict(review: Review) -> dict:
    return {
        "id": str(review.id),
        "booking_id": str(review.booking_id),
        "customer_id": str(review.customer_id),
        "provider_id": str(review.provider_id),
        "service_id": str(review.service_id),
        "serviceName": review.service_name,
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at,
        "updated_at": review.updated_at
    }

# function to convert a dictionary back to a Review object
def dict_to_review(data: dict) -> Review:
    return Review(
        id=UUID(data["id"]),
        booking_id=UUID(data["booking_id"]),
        customer_id=UUID(data["customer_id"]),
        provider_id=UUID(data["provider_id"]),
        service_id=UUID(data["service_id"]),
        service_name=data["serviceName"],
        rating=int(data["rating"]),
        comment=data["comment"],
        created_at=data["created_at"],
        updated_at=data["updated_at"]
    )

# function to load reviews from the JSON file, returning a list of Review objects
def load_reviews() -> list[Review]:
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text("[]")

    content = DATA_FILE.read_text().strip()

    if content == "":
        return []

    reviews_data = json.loads(content)
    reviews = [dict_to_review(review_data) for review_data in reviews_data]
    reviews.reverse()
    return reviews

# function to save a list of Review objects to the JSON file
def save_reviews(reviews: list[Review]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    reviews_data = [review_to_dict(review) for review in reviews]

    DATA_FILE.write_text(json.dumps(reviews_data, indent=4))

# repository function to find all reviews
def find_all() -> list[Review]:
    return load_reviews()

# repository function to find a review by its booking ID
def find_by_booking_id(booking_id: UUID) -> Review | None:
    reviews = load_reviews()

    for review in reviews:
        if review.booking_id == booking_id:
            return review

    return None

# repository function to find all reviews for a specific customer
def find_by_customer_id(customer_id: UUID) -> list[Review]:
    reviews = load_reviews()
    reviews.reverse()  
    return [
        review
        for review in reviews
        if review.customer_id == customer_id
    ]

# repository function to find all reviews for a specific provider
def find_by_provider_id(provider_id: UUID) -> list[Review]:
    reviews = load_reviews()
    reviews.reverse()  

    return [
        review
        for review in reviews
        if review.provider_id == provider_id
    ]

# repository function to find all reviews for a specific service
def find_by_service_id(service_id: UUID) -> list[Review]:
    reviews = load_reviews()

    return [
        review
        for review in reviews
        if review.service_id == service_id
    ]

# repository function to save a new review
def save(review: Review) -> Review:
    reviews = load_reviews()
    reviews.append(review)
    save_reviews(reviews)

    return review

# repository function to delete a review by its ID
def delete_by_id(review_id: UUID) -> None:
    reviews = load_reviews()
    reviews = [review for review in reviews if review.id != review_id]
    save_reviews(reviews)

# repository function to delete all reviews associated with a specific service
def delete_service_reviews(service_id: UUID) -> None:
    reviews = load_reviews()
    reviews = [review for review in reviews if review.service_id != service_id]
    save_reviews(reviews)
