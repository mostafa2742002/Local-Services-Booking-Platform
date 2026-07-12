from flask import Blueprint, render_template

from app.common.security.auth_guard import login_required, role_required
from app.admin.application.admin_dashboard_service import get_admin_dashboard_data


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