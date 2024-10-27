from flask import url_for, render_template
from app.extensions.email_sender import sendgrid_mail
from app.extensions.serializer import generate_token

def send_confirmation_email(user_email):
    token = generate_token(user_email)
    confirm_url = url_for("auth_bp.confirm_email", token=token, _external=True)
    html = render_template("emailTemplates/confirm_email.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    
    sendgrid_mail(to_emails=user_email, subject=subject, html_content=html)