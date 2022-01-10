from functools import wraps

from flask import flash, jsonify, redirect, request, session, url_for
from flask_login import current_user
from jwt import decode
from jwt.exceptions import InvalidTokenError

from flaskr import app
from flaskr.models import Role, User


def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.profile:
            flash("Login first to access the desire route.", "danger")
            return redirect(url_for("users.login_user"))
        if current_user.role.value != Role.ADMIN.value:
            flash("Restricted for only admins.", "danger")
            return redirect(url_for("mains.homepage"))
        return func(*args, **kwargs)
    return wrapper


def is_host(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.profile:
            flash("Login first to access the desire route.", "danger")
            return redirect(url_for("users.login_user"))
        if current_user.role.value != Role.ADMIN.value and current_user.role.value != Role.HOST.value:
            flash("Restricted for only admins and hosts.", "danger")
            return redirect(url_for("mains.homepage"))
        return func(*args, **kwargs)
    return wrapper


def is_general(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.profile:
            flash("Login first to access the desire route.", "danger")
            return redirect(url_for("users.login_user"))
        if current_user.role.value != Role.ADMIN.value and current_user.role.value != Role.GENERAL.value:
            flash("Restricted for only general members.", "danger")
            return redirect(url_for("mains.homepage"))
        return func(*args, **kwargs)
    return wrapper


def is_unbanned(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.profile.is_banned():
            flash("A ban profile can't access the route", "danger")
            return redirect(url_for("mains.homepage"))
        return func(*args, **kwargs)
    return wrapper


def is_verified(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.profile:
            flash("Login first to access the desire route.", "danger")
            return redirect(url_for("users.login_user"))
        if not current_user.is_verified:
            flash("Please verify your account.", "danger")
            return redirect(url_for("mains.homepage"))
        return func(*args, **kwargs)
    return wrapper


def is_token_verified(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.profile:
            flash("Login first to access the desire route.", "danger")
            return redirect(url_for("users.login_user"))
        if current_user.role.value != Role.ADMIN.value:
            flash("Restricted for only admins.", "danger")
            return redirect(url_for("mains.homepage"))
        return func(*args, **kwargs)
    return wrapper


def is_token_verified(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        jwt_token = request.headers.get("Authorization")
        if not jwt_token:
            return jsonify({
                "error": "JTW token is missing."
            }), 403
        try:
            data = decode(jwt_token, app.config.get(
                "JWT_SECRET_KEY"), algorithms=['HS256'])
        except InvalidTokenError:
            return jsonify({
                "error": "Invalid token.",
            }), 403
        except Exception as e:
            return jsonify({
                "error": e.__str__(),
            }), 500
        return func(*args, **kwargs)
    return wrapper
