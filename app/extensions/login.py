from flask_login import LoginManager

login_manager = LoginManager()

def create_app(app):
    login_manager.init_app(app)
    return app