from uuid import UUID

from app.booking.domain.booking_status import BookingStatus

class Booking:

    def __init__(
        self,
        id: UUID,
        customer_id: UUID,
        provider_id: UUID,
        service_id: UUID,
        booking_date: str,
        booking_time: str,
        address: str,
        problem_description: str,
        status: BookingStatus,
        phone_number: str,
        created_at: str,
        updated_at: str
    ):
        self.id = id
        self.customer_id = customer_id
        self.provider_id = provider_id
        self.service_id = service_id
        self.booking_date = booking_date
        self.booking_time = booking_time
        self.address = address
        self.problem_description = problem_description
        self.status = status
        self.phone_number = phone_number
        self.created_at = created_at
        self.updated_at = updated_at

    def get_status_label(self) -> str:
        return self.status.value.title()

    def can_customer_cancel(self) -> bool:
        return self.status == BookingStatus.PENDING

    def can_customer_review(self) -> bool:
        return self.status == BookingStatus.COMPLETED