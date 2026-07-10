from datetime import datetime
from uuid import UUID, uuid4

from app.service.domain.local_service import LocalService
from app.service.infrastructure.service_repository import (
    find_active_services,
    find_by_id,
    find_by_provider_id,
    save
)


def get_available_services() -> list[LocalService]:
    return find_active_services()


def get_service_details(service_id: UUID) -> LocalService:
    service = find_by_id(service_id)

    if service is None:
        raise ValueError("Service not found")

    if not service.is_active:
        raise ValueError("Service is not available")

    return service


def get_provider_services(provider_id: UUID) -> list[LocalService]:
    return find_by_provider_id(provider_id)


def create_local_service(
    provider_id: UUID,
    name: str,
    description: str,
    category: str,
    price: float,
    duration_minutes: int
) -> LocalService:
    now = datetime.now().isoformat(timespec="seconds")

    service = LocalService(
        id=uuid4(),
        provider_id=provider_id,
        name=name,
        description=description,
        category=category,
        price=price,
        duration_minutes=duration_minutes,
        is_active=True,
        created_at=now,
        updated_at=now
    )

    return save(service)