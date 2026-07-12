from dataclasses import dataclass
from uuid import UUID

from app.booking.domain.booking_status import BookingStatus


@dataclass
class Booking:
    id: UUID
    customer_id: UUID
    provider_id: UUID
    service_id: UUID
    booking_date: str
    booking_time: str
    address: str
    problem_description: str
    status: BookingStatus
    created_at: str
    updated_at: str