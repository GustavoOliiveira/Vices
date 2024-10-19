from app.blueprints.user import user_bp
from app.extensions.firestore import db
from flask import jsonify

@user_bp.route("/")
def user():
    users_ref = db.collection("users")
    docs = users_ref.stream()

    users_list = []

    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")
        users_list.append({"id": doc.id, "user": doc.to_dict()})
    return jsonify(users_list)