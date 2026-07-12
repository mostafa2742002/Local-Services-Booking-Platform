from datetime import datetime
from uuid import UUID, uuid4

from app.booking.application.booking_service import get_booking_details
from app.booking.domain.booking_status import BookingStatus
from app.review.domain.review import Review
from app.review.infrastructure.review_repository import (
    find_by_booking_id,
    find_by_customer_id,
    find_by_provider_id,
    find_by_service_id,
    save
)


def create_review(
    customer_id: UUID,
    booking_id: UUID,
    rating: int,
    comment: str
) -> Review:
    booking = get_booking_details(booking_id)

    if booking.customer_id != customer_id:
        raise ValueError("You are not allowed to review this booking")

    if booking.status != BookingStatus.COMPLETED:
        raise ValueError("Only completed bookings can be reviewed")

    existing_review = find_by_booking_id(booking_id)

    if existing_review is not None:
        raise ValueError("Booking already reviewed")

    now = datetime.now().isoformat(timespec="seconds")

    review = Review(
        id=uuid4(),
        booking_id=booking.id,
        customer_id=booking.customer_id,
        provider_id=booking.provider_id,
        service_id=booking.service_id,
        rating=rating,
        comment=comment or "",
        created_at=now,
        updated_at=now
    )

    return save(review)


def get_customer_reviews(customer_id: UUID) -> list[Review]:
    return find_by_customer_id(customer_id)


def get_provider_reviews(provider_id: UUID) -> list[Review]:
    return find_by_provider_id(provider_id)


def get_service_reviews(service_id: UUID) -> list[Review]:
    return find_by_service_id(service_id)


def booking_has_review(booking_id: UUID) -> bool:
    review = find_by_booking_id(booking_id)

    return review is not None