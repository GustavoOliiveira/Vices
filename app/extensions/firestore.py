import firebase_admin
from firebase_admin import credentials, firestore
import os

def create_app():
    data = os.path.abspath(os.path.dirname(__file__)) + "/serviceAccountKey.json"
    cred = credentials.Certificate(data)

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    return firestore.client()

db = create_app()