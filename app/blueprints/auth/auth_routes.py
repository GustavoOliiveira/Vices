from flask import render_template, request, redirect, url_for, session, flash, jsonify
from app.blueprints.auth import auth_bp
from app.forms.user_forms import RegistrationForm, LoginForm
from app.extensions.firestore import db
from app.extensions.encrypt import bcrypt
from app.extensions.oauth import google
from app.extensions.serializer import confirm_token
from app.utils.decorators.auth_decorators import check_is_confirmed, logout_required
from app.models.user_schema import UserSchema
from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import ValidationError
from datetime import datetime
from flask_login import current_user, logout_user, login_required, login_user
from app.utils.user_services import handle_existing_user, handle_new_user
from app.utils.email_services import send_confirmation_email

import requests

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@auth_bp.route("/register", methods=['GET', 'POST'])
@logout_required
def register():
    
    form = RegistrationForm()

    if request.method=='POST' and form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_data = {"username": form.username.data, "email": form.email.data, "password": pw_hash, "provider": "email"}

        try:
            return handle_new_user(user_data)
        except ValidationError as e:
            flash(e.json())

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
                return handle_existing_user(user_data)
            except ValidationError as e:
                flash(e.json())
        else:
            flash("invalid login method")
            return render_template('loginPageFiles/loginPage.html', form=form)
        
    return render_template('loginPageFiles/loginPage.html', form=form)

@auth_bp.route("/callback")
@logout_required
def callback():
    return google.authorize(callback=url_for('auth_bp.authorized', _external=True))

@auth_bp.route("/authorized", methods=['GET', 'POST'])
@logout_required
def authorized():

    # Se a conta já existir -> realizar load_user
    # Se não estiver ativada -> ativar conta

    try:
        response = google.authorized_response()
        if response is None:
            return 'Access denied: reason=%s' % (
                request.args['error'])
        
        session['google_token'] = (response['access_token'], '')
        token = response['access_token']
        validate_token = requests.get("https://www.googleapis.com/oauth2/v1/tokeninfo", params={'access_token': token})

        if validate_token.status_code != 200:
            return "Invalid token."

        token_info = validate_token.json()

        if 'email' not in token_info:
            return "No email found in token info."

        email = token_info['email']
        query = db.collection('users').where(filter=FieldFilter('email', '==', email)).stream()
        result = list(query)

        me = google.get('userinfo')
        new_user_data = me.data
        if result:
            user_data = result[0].to_dict()
            return handle_existing_user(user_data)
        else:
            user_data = {'username': new_user_data['name'], 'email': new_user_data['email'], 'provider': 'gmail'}
            return handle_new_user(user_data)
        
    except ValueError as e:
        print(f'Token inválido ou expirado: {e}')

    return redirect(url_for("auth_bp.login"))

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
        return redirect(url_for("auth_bp.index"))
    
    email = current_user.email
    send_confirmation_email(email)
    flash("A new confirmation email has been sent.", "success")
    return redirect(url_for("auth_bp.inactive"))

@auth_bp.route('/')
@login_required
@check_is_confirmed
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