from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.extensions.firestore import db
from app.extensions.encrypt import bcrypt
from google.cloud.firestore_v1.base_query import FieldFilter

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='data required'), Email(message='invalid email')])
    password = PasswordField('Password', validators=[DataRequired(message='data required')])
    submit = SubmitField('Log In')

    def validate_email(self, email):
        query = db.collection('users').where(filter=FieldFilter('email', '==', email.data)).limit(1).stream()
        #incluir no where provider = email
        if not list(query):
            print('email invalido')
            raise ValidationError('Credenciais incorretas.')
        
    def validate_password(self, password):
        query = db.collection('users').where(filter=FieldFilter('email', '==', self.email.data)).limit(1).stream()
        results = list(query)

        if not results:
            print('email invalido')
            raise ValidationError('Credenciais incorretas.')
        
        user_data = results[0].to_dict()
        if not bcrypt.check_password_hash(user_data.get('password'), password.data):
            raise ValidationError('Credenciais incorretas.')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='data required'), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(message='data required'), Email(message='invalid email')])
    password = PasswordField('Password', validators=[DataRequired(message='data required')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message='data required'), EqualTo('password', message='password must be match')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        query = db.collection('users').where(filter=FieldFilter('email', '==', email.data)).stream()

        if list(query):
            raise ValidationError('Este email já está em uso. Por favor, escolha outro.')
        
    def validate_username(self, username):
        query = db.collection('users').where(filter=FieldFilter('username', '==', username.data)).stream()

        if list(query):
            raise ValidationError('Este nome de usuário já está em uso. Por favor, escolha outro.')