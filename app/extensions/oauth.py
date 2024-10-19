from flask_oauthlib.client import OAuth

google_client_id = '133754314475-4mje7730cculvfntej1mjeara6j4kvni.apps.googleusercontent.com'
google_client_secret = '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'
google_redirect_uri = 'http://127.0.0.1:5000/auth/register/callback'

oauth = OAuth()

def create_app(app):
    oauth.init_app(app)
    return app

google = oauth.remote_app(
    'google',
    consumer_key=google_client_id,
    consumer_secret=google_client_secret,
    request_token_params={
        'scope': 'email profile'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)
