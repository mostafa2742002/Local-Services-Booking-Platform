from app.user.infrastructure.user_repository import find_all as find_all_users
from app.service.infrastructure.service_repository import find_all as find_all_services
from app.booking.infrastructure.booking_repository import find_all as find_all_bookings
from app.review.infrastructure.review_repository import find_all as find_all_reviews
from app.user.infrastructure.user_repository import delete_by_id

def get_admin_dashboard_data() -> dict:
    users = find_all_users()
    services = find_all_services()
    bookings = find_all_bookings()
    reviews = find_all_reviews()

    return {
        "users_count": len(users),
        "services_count": len(services),
        "bookings_count": len(bookings),
        "reviews_count": len(reviews),
        "users": users,
        "services": services,
        "bookings": bookings,
        "reviews": reviews
    }

def get_admin_dashboard_summary() -> dict:
    users = find_all_users()
    services = find_all_services()
    bookings = find_all_bookings()
    reviews = find_all_reviews()

    return {
        "users_count": len(users),
        "services_count": len(services),
        "bookings_count": len(bookings),
        "reviews_count": len(reviews)
    }


def delete_user_by_id(user_id: str) -> None:
    delete_by_id(user_id)