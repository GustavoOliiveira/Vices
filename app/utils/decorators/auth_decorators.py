from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for

def check_is_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_confirmed is False:
            flash("Please confirm your account!", "warning")
            return redirect(url_for("auth_bp.inactive"))
        return func(*args, **kwargs)

    return decorated_function

def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for("auth_bp.index"))
        return func(*args, **kwargs)
    return decorated_function