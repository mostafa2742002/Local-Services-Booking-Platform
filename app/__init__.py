from flask import Flask, render_template
from app.extensions import csrf
from app.admin.application.admin_dashboard_service import get_admin_dashboard_summary
from app.user.api.user_routes import user_bp
from app.service.api.service_routes import service_bp
from app.booking.api.booking_routes import booking_bp
from app.review.api.review_routes import review_bp
from app.admin.api.admin_routes import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    csrf.init_app(app)


    register_blueprints(app)
    register_pages(app)

    return app


def register_blueprints(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(admin_bp)

def register_pages(app):
    @app.get("/")
    def home():
        summary = get_admin_dashboard_summary()
        return render_template("home.html", summary=summary)