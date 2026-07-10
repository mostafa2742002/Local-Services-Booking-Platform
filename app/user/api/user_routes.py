from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from app.user.application.user_service import register_user, login_user
from app.user.api.user_validator import validate_register_data, validate_login_data

user_bp = Blueprint("users", __name__, url_prefix="/auth")



@user_bp.get("/register")
def show_register_page():
    return render_template("auth/register.html")



@user_bp.post("/register")
def submit_register_form():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    errors = validate_register_data(name, email, password, confirm_password)

    if errors:
        for error in errors:
            flash(error, "error")

        return render_template(
            "auth/register.html",
            name=name,
            email=email
        )

    try:
        register_user(
            name=name.strip(),
            email=email.strip().lower(),
            password=password
        )

        flash("Account created successfully. Please login.", "success")
        return redirect(url_for("users.show_login_page"))

    except ValueError as error:
        flash(str(error), "error")

        return render_template(
            "auth/register.html",
            name=name,
            email=email
        )
        
        

@user_bp.get("/login")
def show_login_page():
    return render_template("auth/login.html")


@user_bp.post("/login")
def submit_login_form():
    email = request.form.get("email")
    password = request.form.get("password")

    errors = validate_login_data(email, password)

    if errors:
        for error in errors:
            flash(error, "error")

        return render_template(
            "auth/login.html",
            email=email
        )

    try:
        user = login_user(
            email=email.strip().lower(),
            password=password
        )

        login_user_in_session(user)

        flash("Logged in successfully.", "success")
        return redirect(url_for("home"))

    except ValueError as error:
        flash(str(error), "error")

        return render_template(
            "auth/login.html",
            email=email
        )


@user_bp.get("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("home"))


def login_user_in_session(user):
    session["user_id"] = str(user.id)
    session["user_name"] = user.name
    session["user_role"] = user.role.value