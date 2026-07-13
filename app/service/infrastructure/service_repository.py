import json
from pathlib import Path
from uuid import UUID

from app.service.domain.local_service import LocalService


DATA_FILE = Path("data/services.json")


def service_to_dict(service: LocalService) -> dict:
    return {
        "id": str(service.id),
        "provider_id": str(service.provider_id),
        "name": service.name,
        "description": service.description,
        "category": service.category,
        "price": service.price,
        "duration_minutes": service.duration_minutes,
        "image_filename": service.image_filename,
        "is_active": service.is_active,
        "created_at": service.created_at,
        "updated_at": service.updated_at
    }


def dict_to_service(data: dict) -> LocalService:
    return LocalService(
        id=UUID(data["id"]),
        provider_id=UUID(data["provider_id"]),
        name=data["name"],
        description=data["description"],
        category=data["category"],
        price=float(data["price"]),
        duration_minutes=int(data["duration_minutes"]),
        image_filename=data["image_filename"],
        is_active=bool(data["is_active"]),
        created_at=data["created_at"],
        updated_at=data["updated_at"]
    )


def load_services() -> list[LocalService]:
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text("[]")

    content = DATA_FILE.read_text().strip()

    if content == "":
        return []

    services_data = json.loads(content)

    return [dict_to_service(service_data) for service_data in services_data]


def save_services(services: list[LocalService]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    services_data = [service_to_dict(service) for service in services]

    DATA_FILE.write_text(json.dumps(services_data, indent=4))


def find_all() -> list[LocalService]:
    return load_services()


def find_active_services() -> list[LocalService]:
    services = load_services()

    return [
        service
        for service in services
        if service.is_active
    ]


def find_by_id(service_id: UUID) -> LocalService | None:
    services = load_services()

    for service in services:
        if service.id == service_id:
            return service

    return None


def find_by_provider_id(provider_id: UUID) -> list[LocalService]:
    services = load_services()

    return [
        service
        for service in services
        if service.provider_id == provider_id
    ]


def save(service: LocalService) -> LocalService:
    services = load_services()
    services.append(service)
    save_services(services)

    return service