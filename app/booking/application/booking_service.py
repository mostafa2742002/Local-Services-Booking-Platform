from datetime import datetime
from uuid import UUID, uuid4

from app.booking.domain.booking import Booking
from app.booking.domain.booking_status import BookingStatus
from app.booking.infrastructure import booking_repository
from app.booking.infrastructure.booking_repository import (
    find_by_id,
    find_by_customer_id,
    find_by_provider_id,
    save,
    update
)
from app.service.application.service_service import get_service_details

# service function to create a new booking
def create_booking(
    customer_id: UUID,
    service_id: UUID,
    booking_date: str,
    booking_time: str,
    address: str,
    problem_description: str,
    phone_number: str
) -> Booking:
    local_service = get_service_details(service_id)

    now = datetime.now().isoformat(timespec="seconds")
    # format "YYYY-MM-DDTHH:MM:SS"

    booking = Booking(
        id=uuid4(),
        customer_id=customer_id,
        provider_id=local_service.provider_id,
        service_id=service_id,
        booking_date=booking_date,
        booking_time=booking_time,
        address=address,
        problem_description=problem_description or "",
        status=BookingStatus.PENDING,
        phone_number=phone_number,
        created_at=now,
        updated_at=now
    )

    return save(booking)

# service function to get the details of a specific booking
def get_booking_details(booking_id: UUID) -> Booking:
    booking = find_by_id(booking_id)

    if booking is None:
        raise ValueError("Booking not found")

    return booking

# service function to get all bookings for a specific customer, optionally filtered by status
def get_customer_bookings(customer_id: UUID, status: BookingStatus | None = None):
    bookings = booking_repository.find_by_customer_id(customer_id)

    if status is not None:
        bookings = [
            booking
            for booking in bookings
            if booking.status == status
        ]

    return bookings

# service function to get all bookings for a specific provider, optionally filtered by status
def get_provider_bookings(provider_id: UUID,status: BookingStatus | None = None) -> list[Booking]:
    bookings = find_by_provider_id(provider_id)

    if status is not None:
        bookings = [
            booking
            for booking in bookings
            if booking.status == status
        ]

    return bookings

# service function to cancel a booking for a specific customer
def cancel_booking(customer_id: UUID, booking_id: UUID) -> Booking:
    booking = get_booking_details(booking_id)

    ensure_customer_owns_booking(booking, customer_id)

    if booking.status != BookingStatus.PENDING:
        raise ValueError("Only pending bookings can be cancelled")

    return change_booking_status(booking, BookingStatus.CANCELLED)

# service function to accept a booking for a specific provider
def accept_booking(provider_id: UUID, booking_id: UUID) -> Booking:
    booking = get_booking_details(booking_id)

    ensure_provider_owns_booking(booking, provider_id)

    if booking.status != BookingStatus.PENDING:
        raise ValueError("Only pending bookings can be accepted")

    return change_booking_status(booking, BookingStatus.ACCEPTED)

# service function to reject a booking for a specific provider
def reject_booking(provider_id: UUID, booking_id: UUID) -> Booking:
    booking = get_booking_details(booking_id)

    ensure_provider_owns_booking(booking, provider_id)

    if booking.status != BookingStatus.PENDING:
        raise ValueError("Only pending bookings can be rejected")

    return change_booking_status(booking, BookingStatus.REJECTED)

# service function to start a booking for a specific provider
def start_booking(provider_id: UUID, booking_id: UUID) -> Booking:
    booking = get_booking_details(booking_id)

    ensure_provider_owns_booking(booking, provider_id)

    if booking.status != BookingStatus.ACCEPTED:
        raise ValueError("Only accepted bookings can be started")

    return change_booking_status(booking, BookingStatus.IN_PROGRESS)

# service function to complete a booking for a specific provider
def complete_booking(provider_id: UUID, booking_id: UUID) -> Booking:
    booking = get_booking_details(booking_id)

    ensure_provider_owns_booking(booking, provider_id)

    if booking.status != BookingStatus.IN_PROGRESS:
        raise ValueError("Only in-progress bookings can be completed")

    return change_booking_status(booking, BookingStatus.COMPLETED)

# service function to change the status of a booking and update its timestamp
def change_booking_status(booking: Booking, status: BookingStatus) -> Booking:
    booking.status = status
    booking.updated_at = datetime.now().isoformat(timespec="seconds")

    return update(booking)

# service function to ensure that a customer owns a specific booking
def ensure_customer_owns_booking(booking: Booking, customer_id: UUID) -> None:
    if booking.customer_id != customer_id:
        raise ValueError("You are not allowed to manage this booking")

# service function to ensure that a provider owns a specific booking
def ensure_provider_owns_booking(booking: Booking, provider_id: UUID) -> None:
    if booking.provider_id != provider_id:
        raise ValueError("You are not allowed to manage this booking")