from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_app(app):
    bcrypt.init_app(app)
    return app