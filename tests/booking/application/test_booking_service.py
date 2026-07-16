import pytest
from uuid import uuid4

from app.booking.application import booking_service
from app.booking.domain.booking import Booking
from app.booking.domain.booking_status import BookingStatus
from app.service.domain.local_service import LocalService


def make_service(provider_id=None):
    return LocalService(
        id=uuid4(),
        provider_id=provider_id or uuid4(),
        name="Electrical Repair",
        description="Fix basic home electrical problems.",
        category="Electrical",
        price=350.0,
        duration_minutes=60,
        image_filename="electrical_repair.jpg",
        is_active=True,
        created_at="2026-01-01T10:00:00",
        updated_at="2026-01-01T10:00:00"
    )


def make_booking(
    customer_id=None,
    provider_id=None,
    status=BookingStatus.PENDING
):
    return Booking(
        id=uuid4(),
        customer_id=customer_id or uuid4(),
        provider_id=provider_id or uuid4(),
        service_id=uuid4(),
        booking_date="2026-01-01",
        booking_time="10:30",
        address="Cairo",
        problem_description="Light switch is not working.",
        status=status,
        phone_number="01012345678",
        created_at="2026-01-01T10:00:00",
        updated_at="2026-01-01T10:00:00"
    )


def test_create_booking_creates_pending_booking_with_provider_from_service(monkeypatch):
    provider_id = uuid4()
    customer_id = uuid4()
    service_id = uuid4()
    local_service = make_service(provider_id=provider_id)

    saved_bookings = []

    def fake_get_service_details(received_service_id):
        assert received_service_id == service_id
        return local_service

    def fake_save(booking):
        saved_bookings.append(booking)
        return booking

    monkeypatch.setattr(
        booking_service,
        "get_service_details",
        fake_get_service_details
    )

    monkeypatch.setattr(
        booking_service,
        "save",
        fake_save
    )

    booking = booking_service.create_booking(
        customer_id=customer_id,
        service_id=service_id,
        booking_date="2026-01-01",
        booking_time="10:30",
        address="Cairo",
        problem_description="Light switch is not working.",
        phone_number="01012345678"
    )

    assert booking.customer_id == customer_id
    assert booking.provider_id == provider_id
    assert booking.service_id == service_id
    assert booking.status == BookingStatus.PENDING
    assert booking.phone_number == "01012345678"
    assert len(saved_bookings) == 1


def test_provider_can_move_booking_through_valid_status_flow(monkeypatch):
    provider_id = uuid4()
    booking = make_booking(
        provider_id=provider_id,
        status=BookingStatus.PENDING
    )

    def fake_find_by_id(booking_id):
        return booking

    def fake_update(updated_booking):
        return updated_booking

    monkeypatch.setattr(booking_service, "find_by_id", fake_find_by_id)
    monkeypatch.setattr(booking_service, "update", fake_update)

    booking_service.accept_booking(provider_id, booking.id)
    assert booking.status == BookingStatus.ACCEPTED

    booking_service.start_booking(provider_id, booking.id)
    assert booking.status == BookingStatus.IN_PROGRESS

    booking_service.complete_booking(provider_id, booking.id)
    assert booking.status == BookingStatus.COMPLETED


def test_customer_cannot_cancel_non_pending_booking(monkeypatch):
    customer_id = uuid4()
    booking = make_booking(
        customer_id=customer_id,
        status=BookingStatus.ACCEPTED
    )

    def fake_find_by_id(booking_id):
        return booking

    monkeypatch.setattr(booking_service, "find_by_id", fake_find_by_id)

    with pytest.raises(ValueError, match="Only pending bookings can be cancelled"):
        booking_service.cancel_booking(customer_id, booking.id)


def test_provider_cannot_manage_booking_owned_by_another_provider(monkeypatch):
    real_provider_id = uuid4()
    other_provider_id = uuid4()

    booking = make_booking(
        provider_id=real_provider_id,
        status=BookingStatus.PENDING
    )

    def fake_find_by_id(booking_id):
        return booking

    monkeypatch.setattr(booking_service, "find_by_id", fake_find_by_id)

    with pytest.raises(ValueError, match="You are not allowed to manage this booking"):
        booking_service.accept_booking(other_provider_id, booking.id)