from uuid import UUID

from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from app.common.security.auth_guard import login_required, role_required
from app.booking.application.booking_service import get_booking_details
from app.booking.domain.booking_status import BookingStatus
from app.review.application.review_service import (
    create_review,
    get_customer_reviews,
    booking_has_review
)
from app.review.api.review_validator import validate_create_review_data
from app.service.application.service_service import get_service_details


review_bp = Blueprint("reviews", __name__, url_prefix="/reviews")


@review_bp.get("/create/<booking_id>")
@login_required
@role_required("CUSTOMER")
def show_create_review_page(booking_id):
    parsed_booking_id = parse_uuid(booking_id)

    if parsed_booking_id is None:
        flash("Invalid booking id.", "error")
        return redirect(url_for("bookings.show_customer_bookings"))

    try:
        booking = get_booking_details(parsed_booking_id)
        customer_id = UUID(session["user_id"])

        if booking.customer_id != customer_id:
            flash("You are not allowed to review this booking.", "error")
            return redirect(url_for("bookings.show_customer_bookings"))

        if booking.status != BookingStatus.COMPLETED:
            flash("Only completed bookings can be reviewed.", "error")
            return redirect(url_for("bookings.show_customer_bookings"))

        if booking_has_review(booking.id):
            flash("Booking already reviewed.", "error")
            return redirect(url_for("bookings.show_customer_bookings"))

        return render_template(
            "reviews/create.html",
            booking=booking,
            service_name=get_service_name(booking.service_id)
        )

    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("bookings.show_customer_bookings"))


@review_bp.post("/create/<booking_id>/<service_name>")
@login_required
@role_required("CUSTOMER")
def submit_create_review_form(booking_id, service_name):

    parsed_booking_id = parse_uuid(booking_id)

    if parsed_booking_id is None:
        flash("Invalid booking id.", "error")
        return redirect(url_for("bookings.show_customer_bookings"))

    rating = request.form.get("rating")
    comment = request.form.get("comment")

    errors = validate_create_review_data(rating)

    try:
        booking = get_booking_details(parsed_booking_id)
        customer_id = UUID(session["user_id"])

        if booking.customer_id != customer_id:
            flash("You are not allowed to review this booking.", "error")
            return redirect(url_for("bookings.show_customer_bookings"))

        if booking.status != BookingStatus.COMPLETED:
            flash("Only completed bookings can be reviewed.", "error")
            return redirect(url_for("bookings.show_customer_bookings"))

        if booking_has_review(booking.id):
            flash("Booking already reviewed.", "error")
            return redirect(url_for("bookings.show_customer_bookings"))

    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("bookings.show_customer_bookings"))

    if errors:
        for error in errors:
            flash(error, "error")

        return render_template(
            "reviews/create.html",
            booking=booking,
            service_name=service_name,
            rating=rating,
            comment=comment
        )

    try:
        create_review(
            customer_id=UUID(session["user_id"]),
            booking_id=parsed_booking_id,
            rating=int(rating),
            comment=comment.strip() if comment else "",
            serviceName=service_name
        )

        flash("Review created successfully.", "success")
        return redirect(url_for("reviews.show_customer_reviews"))

    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("bookings.show_customer_bookings"))


@review_bp.get("/my-reviews")
@login_required
@role_required("CUSTOMER")
def show_customer_reviews():
    customer_id = UUID(session["user_id"])
    reviews = get_customer_reviews(customer_id)

    return render_template(
        "reviews/customer_reviews.html",
        review_views=reviews
    )


def build_review_view_models(reviews):
    review_views = []

    for review in reviews:
        review_views.append({
            "review": review,
            "service_name": get_service_name(review.service_id)
        })

    return review_views


def get_service_name(service_id):
    try:
        service = get_service_details(service_id)
        return service.name
    except ValueError:
        return "Unknown service"


def parse_uuid(value: str) -> UUID | None:
    try:
        return UUID(value)
    except ValueError:
        return None