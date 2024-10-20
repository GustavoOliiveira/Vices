from flask import render_template, request, redirect, url_for, session, jsonify, abort, flash
from app.blueprints.auth import auth_bp
from app.forms.user_forms import RegistrationForm, LoginForm
from app.extensions.firestore import db
from app.extensions.encrypt import bcrypt
from app.extensions.oauth import google
from app.models.user_schema import UserSchema
from google.cloud.firestore_v1.base_query import FieldFilter
from pydantic import ValidationError

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

        user_data = {"username": form.username.data, "email": form.email.data, "password": pw_hash, "provider": "email"}
        try:
            new_user = UserSchema(**user_data)
            db.collection("users").add(new_user.model_dump())
            flash("Registration successful!")
            return redirect(url_for('auth_bp.success'))
        except ValidationError as e:
            flash(e.json())
        # print(f"Added document with id {doc_ref.id}")
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
            data = result[0]
            user_data = data.to_dict()
            try:
                user = UserSchema(id=result[0].id, **user_data)
                login_user(user)
                flash("Logged in successfully!")
                return redirect(url_for('auth_bp.index'))
            except ValidationError as e:
                flash(e.json())
        
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