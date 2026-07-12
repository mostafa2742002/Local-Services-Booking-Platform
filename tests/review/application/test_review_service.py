import pytest
from uuid import uuid4

from app.review.application import review_service
from app.booking.domain.booking import Booking
from app.booking.domain.booking_status import BookingStatus


def make_booking(
    customer_id=None,
    provider_id=None,
    service_id=None,
    status=BookingStatus.COMPLETED
):
    return Booking(
        id=uuid4(),
        customer_id=customer_id or uuid4(),
        provider_id=provider_id or uuid4(),
        service_id=service_id or uuid4(),
        booking_date="2026-01-01",
        booking_time="10:30",
        address="Cairo",
        problem_description="Light switch is not working.",
        status=status,
        created_at="2026-01-01T10:00:00",
        updated_at="2026-01-01T10:00:00"
    )


def test_create_review_creates_review_for_completed_booking(monkeypatch):
    customer_id = uuid4()
    provider_id = uuid4()
    service_id = uuid4()

    booking = make_booking(
        customer_id=customer_id,
        provider_id=provider_id,
        service_id=service_id,
        status=BookingStatus.COMPLETED
    )

    saved_reviews = []

    def fake_get_booking_details(booking_id):
        return booking

    def fake_find_by_booking_id(booking_id):
        return None

    def fake_save(review):
        saved_reviews.append(review)
        return review

    monkeypatch.setattr(review_service, "get_booking_details", fake_get_booking_details)
    monkeypatch.setattr(review_service, "find_by_booking_id", fake_find_by_booking_id)
    monkeypatch.setattr(review_service, "save", fake_save)

    review = review_service.create_review(
        customer_id=customer_id,
        booking_id=booking.id,
        rating=5,
        comment="Great service"
    )

    assert review.booking_id == booking.id
    assert review.customer_id == customer_id
    assert review.provider_id == provider_id
    assert review.service_id == service_id
    assert review.rating == 5
    assert review.comment == "Great service"
    assert len(saved_reviews) == 1


def test_create_review_rejects_booking_not_owned_by_customer(monkeypatch):
    customer_id = uuid4()
    other_customer_id = uuid4()

    booking = make_booking(
        customer_id=other_customer_id,
        status=BookingStatus.COMPLETED
    )

    def fake_get_booking_details(booking_id):
        return booking

    monkeypatch.setattr(review_service, "get_booking_details", fake_get_booking_details)

    with pytest.raises(ValueError, match="You are not allowed to review this booking"):
        review_service.create_review(
            customer_id=customer_id,
            booking_id=booking.id,
            rating=5,
            comment="Great service"
        )


def test_create_review_rejects_non_completed_booking(monkeypatch):
    customer_id = uuid4()

    booking = make_booking(
        customer_id=customer_id,
        status=BookingStatus.ACCEPTED
    )

    def fake_get_booking_details(booking_id):
        return booking

    monkeypatch.setattr(review_service, "get_booking_details", fake_get_booking_details)

    with pytest.raises(ValueError, match="Only completed bookings can be reviewed"):
        review_service.create_review(
            customer_id=customer_id,
            booking_id=booking.id,
            rating=5,
            comment="Great service"
        )


def test_create_review_rejects_duplicate_review(monkeypatch):
    customer_id = uuid4()

    booking = make_booking(
        customer_id=customer_id,
        status=BookingStatus.COMPLETED
    )

    existing_review = object()

    def fake_get_booking_details(booking_id):
        return booking

    def fake_find_by_booking_id(booking_id):
        return existing_review

    monkeypatch.setattr(review_service, "get_booking_details", fake_get_booking_details)
    monkeypatch.setattr(review_service, "find_by_booking_id", fake_find_by_booking_id)

    with pytest.raises(ValueError, match="Booking already reviewed"):
        review_service.create_review(
            customer_id=customer_id,
            booking_id=booking.id,
            rating=5,
            comment="Great service"
        )