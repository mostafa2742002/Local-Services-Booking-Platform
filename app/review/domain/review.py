from dataclasses import dataclass
from uuid import UUID


@dataclass
class Review:
    id: UUID
    booking_id: UUID
    customer_id: UUID
    provider_id: UUID
    service_id: UUID
    service_name: str
    rating: int
    comment: str
    created_at: str
    updated_at: str