from firebase_admin import firestore
from flask_login import UserMixin
from datetime import datetime
from app.extensions.firestore import db
from app.extensions.login import login_manager
from google.cloud.firestore_v1.base_query import FieldFilter


class User(UserMixin):
    def __init__(self, username, email, password, provider, id=None, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.provider = provider # email or gmail
        self.created_at = datetime.now()

    @staticmethod
    def get(user):
        user_data = db.collection('users').document(user).get()
        if user_data.exists:
            data = user_data.to_dict()
            user_id = user_data.id
            return User(id=user_id, username=data['username'], email=data['email'], password=data['password'], provider=data['provider'])
        print('User not found')
        return None

@login_manager.user_loader
def load_user(user):
    return User.get(user)