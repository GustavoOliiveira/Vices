import os
from dotenv import load_dotenv

load_dotenv('.env')

class Config:
    SECURITY_PASSWORD_SALT = 'xxx'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    OAUTH_CREDENTIALS = {
        'google': {
            'id': 'YOUR_CLIENT_ID',
            'secret': 'YOUR_CLIENT_SECRET'
        }
    }
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False