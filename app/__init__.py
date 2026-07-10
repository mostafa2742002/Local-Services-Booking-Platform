from flask import Flask, render_template
from app.user.api.user_routes import user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    register_blueprints(app)
    register_pages(app)
    
    return app


def register_blueprints(app):
    app.register_blueprint(user_bp)


def register_pages(app):
    
    @app.get("/")
    def home():
        return render_template("home.html")