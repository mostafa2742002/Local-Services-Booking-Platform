from functools import wraps

from flask import session, flash, redirect, url_for


def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please login first.", "warning")
            return redirect(url_for("users.show_login_page"))

        return route_function(*args, **kwargs)

    return wrapper


def role_required(required_role: str):
    def decorator(route_function):
        @wraps(route_function)
        def wrapper(*args, **kwargs):
            if not session.get("user_id"):
                flash("Please login first.", "warning")
                return redirect(url_for("users.show_login_page"))

            current_role = session.get("user_role")

            if current_role != required_role:
                flash("You are not allowed to access this page.", "error")
                return redirect(url_for("home"))

            return route_function(*args, **kwargs)

        return wrapper

    return decorator