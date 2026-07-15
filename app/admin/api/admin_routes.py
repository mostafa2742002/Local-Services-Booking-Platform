from flask import Blueprint, flash, redirect, render_template, url_for

from app.common.security.auth_guard import login_required, role_required
from app.admin.application.admin_dashboard_service import get_admin_dashboard_data
from app.admin.application.admin_dashboard_service import delete_user_by_id

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.get("/dashboard")
@login_required
@role_required("ADMIN")
def show_admin_dashboard():
    dashboard_data = get_admin_dashboard_data()

    return render_template(
        "admin/dashboard.html",
        dashboard_data=dashboard_data
    )

@admin_bp.get("/delete_user/<user_id>")
@login_required
@role_required("ADMIN")
def delete_user(user_id):
    delete_user_by_id(user_id)
    flash("User deleted successfully", "success")
    return redirect(url_for("admin.show_admin_dashboard"))