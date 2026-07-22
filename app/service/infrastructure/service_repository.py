import json
from pathlib import Path
from uuid import UUID

from app.service.domain.local_service import LocalService


DATA_FILE = Path("data/services.json")

# function to convert a LocalService object to a dictionary for JSON serialization
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

# function to convert a dictionary back to a LocalService object
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

# function to load services from the JSON file, returning a list of LocalService objects
def load_services() -> list[LocalService]:
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text("[]")

    content = DATA_FILE.read_text().strip()

    if content == "":
        return []

    services_data = json.loads(content)
    services = [dict_to_service(service_data) for service_data in services_data]
    services.reverse()
    return services

# function to save a list of LocalService objects to the JSON file
def save_services(services: list[LocalService]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    services_data = [service_to_dict(service) for service in services]

    DATA_FILE.write_text(json.dumps(services_data, indent=4))

# repository function to find all services
def find_all() -> list[LocalService]:
    return load_services()

# repository function to find all active services, optionally filtered by a search query and category
def find_active_services(query: str = "", category: str = "") -> list[LocalService]:
    services = load_services()

    filtered_services = []

    for service in services:
        if not service.is_active:
            continue

        if query and query.lower() not in service.name.lower():
            continue

        if category and category.lower() != service.category.lower():
            continue

        filtered_services.append(service)

    return filtered_services

# repository function to find a service by its ID
def find_by_id(service_id: UUID) -> LocalService | None:
    services = load_services()

    for service in services:
        if service.id == service_id:
            return service

    return None

# repository function to find all services for a specific provider
def find_by_provider_id(provider_id: UUID) -> list[LocalService]:
    services = load_services()
    services.reverse()  

    return [
        service
        for service in services
        if service.provider_id == provider_id
    ]

# repository function to save a new service
def save(service: LocalService) -> LocalService:
    services = load_services()
    services.append(service)
    save_services(services)

    return service

# repository function to update an existing service
def update(service: LocalService) -> LocalService:
    services = load_services()

    for i, existing_service in enumerate(services):
        if existing_service.id == service.id:
            services[i] = service
            save_services(services)
            return service

    raise ValueError("Service not found")

# repository function to delete a service by its ID
def delete(service: LocalService) -> None:
    services = load_services()

    for i, existing_service in enumerate(services):
        if existing_service.id == service.id:
            del services[i]
            save_services(services)
            return

    raise ValueError("Service not found")

# repository function to deletec service image file by its filename
def delete_service_image(image_filename: str) -> None:
    image_path = Path("app/static/images/services") / image_filename

    if image_path.exists():
        image_path.unlink()
    
    