from flask import render_template, request, redirect, url_for, session, jsonify, abort, flash
import requests
import json
from app.blueprints.auth import auth_bp
from app.forms.user_forms import RegistrationForm, LoginForm
from app.extensions.firestore import db
from app.extensions.encrypt import bcrypt
from app.extensions.oauth import google
from app.models.user_schema import User
from google.cloud.firestore_v1.base_query import FieldFilter

from flask_login import current_user, logout_user, login_required, login_user

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth_bp.index'))
    
    form = RegistrationForm()

    if request.method=='POST' and form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        params = {"username": form.username.data, "email": form.email.data, "password": pw_hash, "provider": "email"}
        new_user = User(**params)
        update_time, doc_ref = db.collection("users").add(new_user.to_dict())
        
        # print(f"Added document with id {doc_ref.id}")
        return redirect(url_for('auth_bp.success'))

    return render_template('registerPageFiles/registerPage.html', form=form)

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth_bp.index'))

    form = LoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        # check provider
        query = db.collection('users').where(filter=FieldFilter('email', '==', form.email.data)).where(filter=FieldFilter('provider', '==', 'email')).stream()
        result = list(query)
            
        if result:
            user_data = result[0] #.to_dict()
            user = User(id=user_data.id, username=user_data.get('username'), password=user_data.get('password'), email=user_data.get('email'), provider=user_data.get('provider'))
            login_user(user)
            return redirect(url_for('auth_bp.index'))
        
        flash("invalid login method")
        return render_template('loginPageFiles/loginPage.html', form=form)
        
    return render_template('loginPageFiles/loginPage.html', form=form)

@auth_bp.route("/callback")
def callback():
    return google.authorize(callback=url_for('auth_bp.authorized', _external=True))

@auth_bp.route("/authorized", methods=['GET', 'POST'])
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
    print(session['google_token'])
    me = google.get('userinfo')
    return jsonify({"data": me.data})


@auth_bp.route("/success", methods=['GET'])
def success():
    return render_template('successPageFiles/successPage.html')

@auth_bp.route('/')
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