from flask import flash, url_for, redirect
from app.utils.email_services import send_confirmation_email
from flask_login import login_user
from app.models.user_schema import UserSchema
from app.extensions.firestore import db
from app.utils.email_services import send_confirmation_email

def handle_existing_user(user_data):
    user = UserSchema(**user_data)
    login_user(user)

    if user_data['is_confirmed']:
        flash("Logged in successfully!")
        return redirect(url_for("auth_bp.index"))
    else:
        send_confirmation_email(user_data['email'])
        flash("A confirmation email has been sent via email.", "success")
        return redirect(url_for("auth_bp.inactive"))

def handle_new_user(user_data):
    new_user = UserSchema(**user_data)
    doc_ref = db.collection("users").add(new_user.model_dump())
    generated_id = doc_ref[1].id  # doc_ref retorna uma tupla (write_result, document_reference), pegamos o id da referência

    db.collection("users").document(generated_id).update({"id": generated_id})

    email = user_data['email']
    send_confirmation_email(email)

    new_user.id = generated_id
    login_user(new_user)
    
    flash("A confirmation email has been sent via email.", "success")
    return redirect(url_for("auth_bp.inactive"))