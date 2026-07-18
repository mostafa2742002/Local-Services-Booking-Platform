from app.user.infrastructure.user_repository import find_all as find_all_users
from app.service.infrastructure.service_repository import find_all as find_all_services
from app.booking.infrastructure.booking_repository import find_all as find_all_bookings
from app.review.infrastructure.review_repository import find_all as find_all_reviews
from app.user.infrastructure import user_repository
from app.review.infrastructure import review_repository
from app.booking.infrastructure import booking_repository
from app.service.infrastructure import service_repository

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
    user = user_repository.find_by_id(user_id)
    if not user:
        raise ValueError("User not found")
    print(f"Deleting user with ID: {user_id} and role: {user.role.value}")
    if user.role.value == "PROVIDER":
        handle_delete_provider(user_id)
        
    elif user.role.value == "CUSTOMER":
        handle_delete_customer(user_id)
        
    
    


def handle_delete_provider(user_id: str) -> None:
    # Delete all services associated with the provider
    services = find_all_services()
    provider_services = [service for service in services if str(service.provider_id) == str(user_id)]
    
    for service in provider_services:
        # Delete all bookings associated with the service
        bookings = find_all_bookings()
        service_bookings = [booking for booking in bookings if str(booking.service_id) == str(service.id)]
        
        for booking in service_bookings:
            # Delete all reviews associated with the booking
            reviews = find_all_reviews()
            booking_reviews = [review for review in reviews if str(review.booking_id) == str(booking.id)]
            
            for review in booking_reviews:
                # Delete the review
                review_repository.delete_by_id(review.id)
            
            # Delete the booking            
            booking_repository.delete_by_id(booking.id)
        
        # Delete the service
        service_repository.delete_service_image(service.image_filename)
        service_repository.delete(service)
    
    # delete the provider user
    user_repository.delete_by_id(user_id)
    


def handle_delete_customer(user_id: str) -> None:
    # Delete all bookings associated with the customer
    bookings = find_all_bookings()
    customer_bookings = [booking for booking in bookings if str(booking.customer_id) == str(user_id)]
    
    for booking in customer_bookings:
        # Delete all reviews associated with the booking
        reviews = find_all_reviews()
        booking_reviews = [review for review in reviews if str(review.booking_id) == str(booking.id)]
        
        for review in booking_reviews:
            # Delete the review
            review_repository.delete_by_id(review.id)
        
        # Delete the booking            
        booking_repository.delete_by_id(booking.id)
    
    # delete the customer user
    user_repository.delete_by_id(user_id)