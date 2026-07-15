import pytest
from uuid import uuid4

from app.service.application import service_service
from app.service.domain.local_service import LocalService


def make_service(is_active=True):
    return LocalService(
        id=uuid4(),
        provider_id=uuid4(),
        name="Home Cleaning",
        description="General home cleaning service",
        category="Cleaning",
        price=250.0,
        duration_minutes=60,
        image_filename="home_cleaning.jpg",
        is_active=is_active,
        created_at="2026-01-01T10:00:00",
        updated_at="2026-01-01T10:00:00"
    )


def make_image(filename="plumbing_repair.jpg"):
    class FakeImage:
        def __init__(self, name):
            self.filename = name
            self.saved_path = None

        def save(self, path):
            self.saved_path = path

    return FakeImage(filename)


def test_get_available_services_returns_active_services(monkeypatch):
    active_services = [
        make_service(is_active=True),
        make_service(is_active=True)
    ]

    def fake_find_active_services(query="", category=""):
        return active_services

    monkeypatch.setattr(
        service_service,
        "find_active_services",
        fake_find_active_services
    )

    result = service_service.get_available_services()

    assert result == active_services


def test_get_service_details_returns_service_when_active(monkeypatch):
    existing_service = make_service(is_active=True)

    def fake_find_by_id(service_id):
        return existing_service

    monkeypatch.setattr(
        service_service,
        "find_by_id",
        fake_find_by_id
    )

    result = service_service.get_service_details(existing_service.id)

    assert result == existing_service


def test_get_service_details_rejects_missing_service(monkeypatch):
    def fake_find_by_id(service_id):
        return None

    monkeypatch.setattr(
        service_service,
        "find_by_id",
        fake_find_by_id
    )

    with pytest.raises(ValueError, match="Service not found"):
        service_service.get_service_details(uuid4())


def test_create_local_service_creates_active_service(monkeypatch):
    saved_services = []

    def fake_save(service):
        saved_services.append(service)
        return service

    monkeypatch.setattr(
        service_service,
        "save",
        fake_save
    )

    provider_id = uuid4()
    image = make_image()

    service = service_service.create_local_service(
        provider_id=provider_id,
        name="Plumbing Repair",
        description="Fix common plumbing problems at home.",
        category="Plumbing",
        price=300.0,
        duration_minutes=60,
        image=image
    )

    assert service.provider_id == provider_id
    assert service.name == "Plumbing Repair"
    assert service.description == "Fix common plumbing problems at home."
    assert service.category == "Plumbing"
    assert service.price == 300.0
    assert service.duration_minutes == 60
    assert service.image_filename == image.filename
    assert service.is_active is True
    assert len(saved_services) == 1
    assert image.saved_path.endswith(image.filename)