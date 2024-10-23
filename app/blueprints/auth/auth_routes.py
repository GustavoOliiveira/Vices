from flask import render_template, request, redirect, url_for, session, jsonify, abort, flash
from app.blueprints.auth import auth_bp
from app.forms.user_forms import RegistrationForm, LoginForm
from app.extensions.firestore import db
from app.extensions.encrypt import bcrypt
from app.extensions.oauth import google
from app.extensions.serializer import generate_token, confirm_token
from app.extensions.email_sender import sendgrid_mail
from app.utils.decorators.auth_decorators import check_is_confirmed, logout_required
from app.models.user_schema import UserSchema
from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import ValidationError
from datetime import datetime
from functools import wraps
from flask_login import current_user, logout_user, login_required, login_user

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@auth_bp.route("/register", methods=['GET', 'POST'])
@logout_required
def register():
    
    form = RegistrationForm()

    if request.method=='POST' and form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_email = form.email.data
        user_data = {"username": form.username.data, "email": user_email, "password": pw_hash, "provider": "email"}
        try:
            new_user = UserSchema(**user_data)
            doc_ref = db.collection("users").add(new_user.model_dump())
            generated_id = doc_ref[1].id  # doc_ref retorna uma tupla (write_result, document_reference), pegamos o id da referência

            # Agora atualiza o documento com o ID gerado dentro de um campo "id"
            db.collection("users").document(generated_id).update({"id": generated_id})
            token = generate_token(user_email)

            confirm_url = url_for("auth_bp.confirm_email", token=token, _external=True)
            html = render_template("emailTemplates/confirm_email.html", confirm_url=confirm_url)
            subject = "Please confirm your email"
            sendgrid_mail(to_emails=user_email, subject=subject, html_content=html)

            user_data = db.collection("users").document(generated_id).get().to_dict()

            user = UserSchema(**user_data) #id=result[0].id,
            login_user(user)

            flash("A confirmation email has been sent via email.", "success")
            return redirect(url_for("auth_bp.inactive"))

        except ValidationError as e:
            flash(e.json())
        # print(f"Added document with id {doc_ref.id}")
    return render_template('registerPageFiles/registerPage.html', form=form)

@auth_bp.route("/login", methods=['GET', 'POST'])
@logout_required
def login():

    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        # check provider
        query = db.collection('users').where(filter=FieldFilter('email', '==', form.email.data)).where(filter=FieldFilter('provider', '==', 'email')).stream()
        result = list(query)
            
        if result:
            data = result[0]
            user_data = data.to_dict()
            try:
                user = UserSchema(**user_data) #id=result[0].id,
                login_user(user)
                #sendgrid_mail(form.email.data, "teste", "teste2")
                flash("Logged in successfully!")
                return redirect(url_for('auth_bp.index'))
            except ValidationError as e:
                flash(e.json())
        
        flash("invalid login method")
        return render_template('loginPageFiles/loginPage.html', form=form)
        
    return render_template('loginPageFiles/loginPage.html', form=form)

@auth_bp.route("/callback")
@logout_required
def callback():
    return google.authorize(callback=url_for('auth_bp.authorized', _external=True))

@auth_bp.route("/authorized", methods=['POST'])
@logout_required
def authorized():

    response = google.authorized_response()
    if response is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    
    #verificar se o token é válido.
    #url = requests.get("https://www.googleapis.com/oauth2/v1/tokeninfo", params={'access_token': "session['google_token']"}) #session['google_token']
    #print(url)
    session['google_token'] = (response['access_token'], '')
    me = google.get('userinfo')
    #return jsonify({"data": me.data})
    return redirect(url_for("auth_bp.index"))

@auth_bp.route("/inactive")
@login_required
def inactive():
    if current_user.is_confirmed:
        return redirect(url_for("auth_bp.index"))
    return render_template("registerPageFiles/inactive.html")

@auth_bp.route("/confirm/<token>")
@login_required
def confirm_email(token):
    if current_user.is_confirmed:
        flash("Account already confirmed.", "success")
        return redirect(url_for("auth_bp.index"))
    email = confirm_token(token)
    user_data = db.collection('users').document(current_user.id).get().to_dict()
    if user_data.get('email') == email:
        db.collection("users").document(current_user.id).update({"is_confirmed": True, "confirmed_at": datetime.now()})
        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("auth_bp.index"))

@auth_bp.route("/resend")
@login_required
def resend_confirmation():
    if current_user.is_confirmed:
        flash("Your account has already been confirmed.", "success")
        return redirect(url_for("core.home"))
    token = generate_token(current_user.email)
    confirm_url = url_for("auth_bp.confirm_email", token=token, _external=True)
    html = render_template("emailTemplates/confirm_email.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    sendgrid_mail(to_emails=current_user.email, subject=subject, html_content=html)
    flash("A new confirmation email has been sent.", "success")
    return redirect(url_for("auth_bp.inactive"))

@auth_bp.route('/')
@check_is_confirmed
@login_required
def index():
    if current_user.is_authenticated:
        return "authorized"
    # if 'google_token' in session:
    #     me = google.get('userinfo')
    #     return jsonify({"data": me.data})
    return redirect(url_for('auth_bp.login'))

@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    session.pop('google_token', None)
    flash("logout successful!")
    return redirect(url_for('auth_bp.login'))