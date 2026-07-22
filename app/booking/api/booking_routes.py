from uuid import UUID

from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from app.booking.domain.booking_status import BookingStatus
from app.booking.domain.booking_status import BookingStatus
from app.common.security.auth_guard import login_required, role_required
from app.service.application.service_service import get_service_details
from app.booking.application.booking_service import (
    create_booking,
    get_customer_bookings,
    get_provider_bookings,
    cancel_booking,
    accept_booking,
    reject_booking,
    start_booking,
    complete_booking
)
from app.booking.api.booking_validator import validate_create_booking_data


booking_bp = Blueprint("bookings", __name__, url_prefix="/bookings")

# show the create booking page for a specific service
@booking_bp.get("/create/<service_id>")
@login_required
@role_required("CUSTOMER")
def show_create_booking_page(service_id):
    parsed_service_id = parse_uuid(service_id)

    if parsed_service_id is None:
        flash("Invalid service id.", "error")
        return redirect(url_for("services.list_services"))

    try:
        service = get_service_details(parsed_service_id)

        return render_template(
            "bookings/create.html",
            service=service
        )

    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("services.list_services"))

# handle the submission of the create booking form
@booking_bp.post("/create/<service_id>")
@login_required
@role_required("CUSTOMER")
def submit_create_booking_form(service_id):
    parsed_service_id = parse_uuid(service_id)

    if parsed_service_id is None:
        flash("Invalid service id.", "error")
        return redirect(url_for("services.list_services"))

    booking_date = request.form.get("booking_date")
    booking_time = request.form.get("booking_time")
    address = request.form.get("address")
    problem_description = request.form.get("problem_description")
    phone_number = request.form.get("phone_number")

    errors = validate_create_booking_data(
        booking_date=booking_date,
        booking_time=booking_time,
        address=address,
        phone_number=phone_number,
    )

    try:
        service = get_service_details(parsed_service_id)

    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("services.list_services"))

    if errors:
        for error in errors:
            flash(error, "error")

        return render_template(
            "bookings/create.html",
            service=service,
            booking_date=booking_date,
            booking_time=booking_time,
            address=address,
            problem_description=problem_description,
            phone_number=phone_number
        )

    customer_id = UUID(session["user_id"])

    create_booking(
        customer_id=customer_id,
        service_id=parsed_service_id,
        booking_date=booking_date.strip(),
        booking_time=booking_time.strip(),
        address=address.strip(),
        problem_description=problem_description,
        phone_number=phone_number.strip()
    )

    flash("Booking request created successfully.", "success")
    return redirect(url_for("bookings.show_customer_bookings"))

# show the bookings for the logged-in customer
@booking_bp.get("/my-bookings")
@login_required
@role_required("CUSTOMER")
def show_customer_bookings():
    customer_id = UUID(session["user_id"])

    selected_status = request.args.get(
        "status",
        default="all",
        type=str
    ).strip().upper()

    booking_status = None

    if selected_status != "ALL":
        try:
            booking_status = BookingStatus(selected_status)
        except ValueError:
            selected_status = "ALL"

    bookings = get_customer_bookings(
        customer_id=customer_id,
        status=booking_status
    )

    return render_template(
        "bookings/customer_bookings.html",
        bookings=bookings,
        status_options=list(BookingStatus),
        selected_status=selected_status.lower()
    )

# cancel a booking for the logged-in customer
@booking_bp.post("/<booking_id>/cancel")
@login_required
@role_required("CUSTOMER")
def cancel_customer_booking(booking_id):
    parsed_booking_id = parse_uuid(booking_id)

    if parsed_booking_id is None:
        flash("Invalid booking id.", "error")
        return redirect(url_for("bookings.show_customer_bookings"))

    customer_id = UUID(session["user_id"])

    try:
        cancel_booking(
            customer_id=customer_id,
            booking_id=parsed_booking_id
        )

        flash("Booking cancelled successfully.", "success")

    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("bookings.show_customer_bookings"))

# show the bookings for the logged-in provider
@booking_bp.get("/provider/requests")
@login_required
@role_required("PROVIDER")
def show_provider_bookings():
    provider_id = UUID(session["user_id"])

    selected_status = request.args.get(
        "status",
        default="all",
        type=str
    ).strip().upper()

    booking_status = None

    if selected_status != "ALL":
        try:
            booking_status = BookingStatus(selected_status)
        except ValueError:
            selected_status = "ALL"

    bookings = get_provider_bookings(
        provider_id=provider_id,
        status=booking_status
    )

    return render_template(
        "bookings/provider_bookings.html",
        bookings=bookings,
        status_options=list(BookingStatus),
        selected_status=selected_status.lower()
    )


@booking_bp.post("/provider/<booking_id>/accept")
@login_required
@role_required("PROVIDER")
def accept_provider_booking(booking_id):
    return handle_provider_booking_action(
        booking_id=booking_id,
        action_function=accept_booking,
        success_message="Booking accepted successfully."
    )

# Reject a booking for the logged-in provider
@booking_bp.post("/provider/<booking_id>/reject")
@login_required
@role_required("PROVIDER")
def reject_provider_booking(booking_id):
    return handle_provider_booking_action(
        booking_id=booking_id,
        action_function=reject_booking,
        success_message="Booking rejected successfully."
    )


# Start a booking for the logged-in provider
@booking_bp.post("/provider/<booking_id>/start")
@login_required
@role_required("PROVIDER")
def start_provider_booking(booking_id):
    return handle_provider_booking_action(
        booking_id=booking_id,
        action_function=start_booking,
        success_message="Booking started successfully."
    )

# Complete a booking for the logged-in provider
@booking_bp.post("/provider/<booking_id>/complete")
@login_required
@role_required("PROVIDER")
def complete_provider_booking(booking_id):
    return handle_provider_booking_action(
        booking_id=booking_id,
        action_function=complete_booking,
        success_message="Booking completed successfully."
    )

# Helper function to handle provider booking actions
def handle_provider_booking_action(booking_id, action_function, success_message):
    parsed_booking_id = parse_uuid(booking_id)

    if parsed_booking_id is None:
        flash("Invalid booking id.", "error")
        return redirect(url_for("bookings.show_provider_bookings"))

    provider_id = UUID(session["user_id"])

    try:
        action_function(
            provider_id=provider_id,
            booking_id=parsed_booking_id
        )

        flash(success_message, "success")

    except ValueError as error:
        flash(str(error), "error")

    return redirect(url_for("bookings.show_provider_bookings"))

# Helper function to parse a string into a UUID
def parse_uuid(value: str) -> UUID | None:
    try:
        return UUID(value)
    except ValueError:
        return None