import json
from pathlib import Path
from uuid import UUID

from app.booking.domain.booking import Booking
from app.booking.domain.booking_status import BookingStatus


DATA_FILE = Path("data/bookings.json")

# function to convert a Booking object to a dictionary for JSON serialization
def booking_to_dict(booking: Booking) -> dict:
    return {
        "id": str(booking.id),
        "customer_id": str(booking.customer_id),
        "provider_id": str(booking.provider_id),
        "service_id": str(booking.service_id),
        "booking_date": booking.booking_date,
        "booking_time": booking.booking_time,
        "address": booking.address,
        "problem_description": booking.problem_description,
        "status": booking.status.value,
        "phone_number": booking.phone_number,
        "created_at": booking.created_at,
        "updated_at": booking.updated_at
    }

# function to convert a dictionary back to a Booking object
def dict_to_booking(data: dict) -> Booking:
    return Booking(
        id=UUID(data["id"]),
        customer_id=UUID(data["customer_id"]),
        provider_id=UUID(data["provider_id"]),
        service_id=UUID(data["service_id"]),
        booking_date=data["booking_date"],
        booking_time=data["booking_time"],
        address=data["address"],
        problem_description=data["problem_description"],
        status=BookingStatus(data["status"]),
        phone_number=data["phone_number"],
        created_at=data["created_at"],
        updated_at=data["updated_at"]
    )

# function to load bookings from the JSON file, returning a list of Booking objects
def load_bookings() -> list[Booking]:
    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text("[]")

    content = DATA_FILE.read_text().strip()

    if content == "":
        return []

    bookings_data = json.loads(content)
    bookings = [dict_to_booking(booking_data) for booking_data in bookings_data]
    bookings.reverse()
    return bookings

# function to save a list of Booking objects to the JSON file
def save_bookings(bookings: list[Booking]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    bookings_data = [booking_to_dict(booking) for booking in bookings]

    DATA_FILE.write_text(json.dumps(bookings_data, indent=4))

# repository function to find all bookings
def find_all() -> list[Booking]:
    return load_bookings()

# repository function to find a booking by its ID
def find_by_id(booking_id: UUID) -> Booking | None:
    bookings = load_bookings()

    for booking in bookings:
        if booking.id == booking_id:
            return booking

    return None

# repository function to find all bookings for a specific customer
def find_by_customer_id(customer_id: UUID) -> list[Booking]:
    bookings = load_bookings()

    return [
        booking
        for booking in bookings
        if booking.customer_id == customer_id
    ]

# repository function to find all bookings for a specific provider
def find_by_provider_id(provider_id: UUID) -> list[Booking]:
    bookings = load_bookings()

    return [
        booking
        for booking in bookings
        if booking.provider_id == provider_id
    ]

# repository function to save a new booking
def save(booking: Booking) -> Booking:
    bookings = load_bookings()
    bookings.append(booking)
    save_bookings(bookings)

    return booking

# repository function to update an existing booking
def update(updated_booking: Booking) -> Booking:
    bookings = load_bookings()

    for index, booking in enumerate(bookings):
        if booking.id == updated_booking.id:
            bookings[index] = updated_booking
            save_bookings(bookings)
            return updated_booking

    raise ValueError("Booking not found")

# repository function to delete a booking by its ID
def delete_by_id(booking_id: UUID) -> None:
    bookings = load_bookings()
    bookings = [booking for booking in bookings if booking.id != booking_id]
    save_bookings(bookings)

# repository function to delete all bookings associated with a specific service
def delete_service_appointments(service_id: UUID) -> None:
    bookings = load_bookings()
    bookings = [booking for booking in bookings if booking.service_id != service_id]
    save_bookings(bookings)
    
