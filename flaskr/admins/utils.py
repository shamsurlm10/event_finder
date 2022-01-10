from datetime import datetime, timedelta

from flask import flash, redirect, url_for
from flaskr import db
from flaskr.models import AccountRestriction, Notification, Profile
from flaskr.notifications.utils import NotificationMessage


def __ban_user(form_data, id: int) -> bool:
    profile = Profile.query.get(id)
    if profile.is_banned():
        flash("Cannot ban a user who is already banned.", "danger")
        return None
    days = form_data.get("days")
    reason = form_data.get("reason")
    try:
        expire_date = datetime.utcnow() + timedelta(days=int(days))
    except ValueError:
        flash("Enter the duration of the banned.", "danger")
        return redirect(url_for("profiles.view_profile", id=id))
    acc_restriction = AccountRestriction(expire_date, reason, id)
    db.session.add(acc_restriction)
    # push notification
    notification = Notification(NotificationMessage.ban_user(
        reason), url_for("mains.homepage"), id)
    db.session.add(notification)
    db.session.commit()
    flash(f"Account has been banned for {days} days.", "success")
    return profile
