from flask import Flask
from app.blueprints.user import user_bp
from app.blueprints.main import main_bp
from app.blueprints.auth import auth_bp

def register_blueprints(app: Flask):
    app.register_blueprint(user_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
