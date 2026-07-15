from datetime import datetime
import os
from uuid import UUID, uuid4

from app.service.domain.local_service import LocalService
from app.service.infrastructure.service_repository import (
    find_active_services,
    find_by_id,
    find_by_provider_id,
    save,
    update
)


def get_available_services(query: str = "", category: str = "") -> list[LocalService]:
    return find_active_services(query=query, category=category)


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
    duration_minutes: int,
    image: any
) -> LocalService:
    now = datetime.now().isoformat(timespec="seconds")

    image.save(os.path.join("app/static/images/services", image.filename))

    service = LocalService(
        id=uuid4(),
        provider_id=provider_id,
        name=name,
        description=description,
        category=category,
        price=price,
        duration_minutes=duration_minutes,
        image_filename=image.filename,
        is_active=True,
        created_at=now,
        updated_at=now
    )

    return save(service)


def get_all_categories() -> list[str]:
    services = find_active_services()
    categories = [service.category for service in services]
    return sorted(categories)


def toggle_service_active_status_service(service_id: UUID) -> None:
    print(f"Toggling active status for service with ID: {service_id}")
    service = find_by_id(service_id)

    if service is None:
        raise ValueError("Service not found")

    service.is_active = not service.is_active
    service.updated_at = datetime.now().isoformat(timespec="seconds")
    update(service)