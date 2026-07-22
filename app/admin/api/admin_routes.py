from uuid import UUID
from flask import Blueprint, flash, redirect, render_template, url_for
from app.common.security.auth_guard import login_required, role_required
from app.admin.application.admin_dashboard_service import get_admin_dashboard_data
from app.admin.application.admin_dashboard_service import delete_user_by_id
from app.service.application.service_service import toggle_service_active_status_service


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# get the admin dashboard
@admin_bp.get("/dashboard")
@login_required
@role_required("ADMIN")
def show_admin_dashboard():
    dashboard_data = get_admin_dashboard_data()

    return render_template(
        "admin/dashboard.html",
        dashboard_data=dashboard_data
    )

# delete a user by id
@admin_bp.get("/delete_user/<user_id>")
@login_required
@role_required("ADMIN")
def delete_user(user_id):
    delete_user_by_id(UUID(user_id))
    flash("User deleted successfully", "success")
    return redirect(url_for("admin.show_admin_dashboard"))

# toggle the active status of a service by id
@admin_bp.get("/active_switch/<service_id>")    
@login_required
@role_required("ADMIN")
def toggle_service_active_status(service_id):

    try:
        toggle_service_active_status_service(UUID(service_id))
        flash("Service active status toggled successfully", "success")
    except ValueError as e:
        flash(str(e), "error")

    return redirect(url_for("admin.show_admin_dashboard"))
