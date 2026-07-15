from dataclasses import dataclass
from uuid import UUID


@dataclass
class LocalService:
    id: UUID
    provider_id: UUID
    name: str
    description: str
    category: str
    price: float
    duration_minutes: int
    image_filename: str
    is_active: bool
    created_at: str
    updated_at: str