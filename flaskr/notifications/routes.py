from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flaskr.admins.forms import *
from flaskr.models import Notification
from sqlalchemy import desc

notifications = Blueprint("notifications", __name__)


@notifications.route("/notifications")
@login_required
def get_notifications():
    notifications = Notification.query.filter_by(
        profile_id=current_user.profile.id).order_by(desc(Notification.created_at))[:20]
    return render_template("notifications/notification.html", notifications=notifications)


@notifications.route("/notification/mark-read/<int:id>")
@login_required
def mark_read(id: int):
    notification = Notification.query.get(id)
    if notification.profile.id != current_user.profile.id:
        flash("Not authorized for this action.", "danger")
    else:
        notification.mark_read()
    return redirect(url_for("notifications.get_notifications"))


@notifications.route("/notification/mark-read-and-go/<int:id>")
@login_required
def mark_read_and_go(id: int):
    notification = Notification.query.get(id)
    # If the user is not the owner of that notification
    if notification.profile.id != current_user.profile.id:
        flash("Not authorized for this action.", "danger")
    elif not notification.is_readed:
        notification.mark_read()
    if notification.link == "":
        return redirect(url_for("notifications.get_notifications"))
    return redirect(notification.link)


@notifications.route("/notification/mark_all")
@login_required
def mark_all():
    notifications = current_user.profile.notifications
    for notification in notifications:
        if not notification.is_readed:
            notification.mark_read()
    return redirect(url_for("notifications.get_notifications"))
