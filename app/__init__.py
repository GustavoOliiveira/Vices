from flask import Flask
from config import Config, DevelopmentConfig
from app.extensions import encrypt, oauth, login
from app.blueprints import register_blueprints

app = Flask(__name__, template_folder='templates')

def create_app(config_class=Config):
    app.config.from_object(config_class)

    # carregando extensões
    login.create_app(app)
    encrypt.create_app(app)
    oauth.create_app(app)

    # registrando rotas
    register_blueprints(app)

    return app