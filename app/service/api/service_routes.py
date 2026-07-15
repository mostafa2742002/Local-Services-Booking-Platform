from uuid import UUID

from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from app.common.security.auth_guard import login_required, role_required
from app.service.application.service_service import (
    get_available_services,
    get_service_details,
    get_provider_services,
    create_local_service,
    get_all_categories
)
from app.service.api.service_validator import validate_create_service_data


service_bp = Blueprint("services", __name__, url_prefix="/services")


@service_bp.get("/")
def list_services():
    services = get_available_services()
    categories = get_all_categories()  
    return render_template(
        "services/list.html",
        services=services,
        categories=categories
    )


@service_bp.post("/")
def list_services_with_filters():
    query = request.form.get("search", "")
    filter_category = request.form.get("category", "")
    services = get_available_services(query=query, category=filter_category)
    categories = get_all_categories()  
    return render_template(
        "services/list.html",
        services=services,
        categories=categories
    )

@service_bp.get("/<service_id>")
def show_service_details(service_id):
    try:
        service = get_service_details(UUID(service_id))

        return render_template(
            "services/details.html",
            service=service
        )

    except ValueError as error:
        flash(str(error), "error")
        return redirect(url_for("services.list_services"))


@service_bp.get("/provider/my-services")
@login_required
@role_required("PROVIDER")
def show_provider_services():
    provider_id = UUID(session["user_id"])
    services = get_provider_services(provider_id)

    return render_template(
        "services/provider_services.html",
        services=services
    )


@service_bp.get("/provider/create")
@login_required
@role_required("PROVIDER")
def show_create_service_page():
    return render_template("services/create.html")


@service_bp.post("/provider/create")
@login_required
@role_required("PROVIDER")
def submit_create_service_form():
    name = request.form.get("name")
    description = request.form.get("description")
    category = request.form.get("category")
    price = request.form.get("price")
    duration_minutes = request.form.get("duration_minutes")
    image = request.files.get("image")

    errors = validate_create_service_data(
        name=name,
        description=description,
        category=category,
        price=price,
        duration_minutes=duration_minutes,
        image=image
    )

    if errors:
        for error in errors:
            flash(error, "error")

        return render_template(
            "services/create.html",
            name=name,
            description=description,
            category=category,
            price=price,
            duration_minutes=duration_minutes
        )

    provider_id = UUID(session["user_id"])

    create_local_service(
        provider_id=provider_id,
        name=name.strip(),
        description=description.strip(),
        category=category.strip(),
        price=float(price),
        duration_minutes=int(duration_minutes),
        image=image
    )

    flash("Service created successfully.", "success")
    return redirect(url_for("services.show_provider_services"))