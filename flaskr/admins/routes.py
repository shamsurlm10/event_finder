from datetime import datetime, timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flaskr import db
from flaskr.admins.forms import *
from flaskr.admins.utils import __ban_user
from flaskr.decorators import is_admin
from flaskr.models import (AccountRestriction, Complain, Event, Notification,
                           Profile, PromotionPending, Role, User)
from flaskr.notifications.utils import NotificationMessage
from sqlalchemy import desc

admins = Blueprint("admins", __name__, url_prefix="/admins")


@admins.route("/")
@admins.route("/dashboard")
@login_required
@is_admin
def dashboard():
    users = User.query.order_by(desc(User.created_at))[:4]
    profiles = Profile.query.all()
    events = Event.query.order_by(desc(Event.created_at))[:3]
    reqs = PromotionPending.query.all()
    complains = Complain.query.all()

    # for the pie chart
    data = {
        "Banned Users": 0,
        "Unverified Users": 0,
        "Host Users": 0,
        "General Users": 0,
        "Admins": 0,
    }
    for i in range(len(profiles)):
        if profiles[i].banned != None:
            data["Banned Users"] = data.get("Banned Users")+1
        if not profiles[i].user.is_verified:
            data["Unverified Users"] = data.get("Unverified Users")+1
        if profiles[i].user.role == Role.ADMIN:
            data["Host Users"] = data.get("Host Users")+1
        if profiles[i].user.role == Role.HOST:
            data["Admins"] = data.get("Admins")+1
        if profiles[i].user.role == Role.GENERAL:
            data["General Users"] = data.get("General Users")+1

    return render_template("admins/dashboard.html",
                           active="dashboard", users=users,
                           events=events, data=data, len=len,
                           length_of_req_pending=len(reqs),
                           length_of_complains=len(complains))


@admins.route("/hosts")
@login_required
@is_admin
def view_hosts():
    hosts = User.query.filter_by(role=Role.HOST).all()
    return render_template("admins/view_hosts.html",
                           active="view_hosts",
                           hosts=hosts,
                           total_hosts=len(hosts))


@admins.route("/demote-host/<int:id>")
@login_required
@is_admin
def demote_host(id: int):
    user = User.query.get(id)
    user.role = Role.GENERAL
    db.session.commit()
    flash("The user is demoted to general member.", "info")
    return redirect(url_for("profiles.view_profile", id=id))


@admins.route("/promote-host/<int:id>")
@login_required
@is_admin
def promote_host(id: int):
    user = User.query.get(id)
    user.role = Role.HOST
    db.session.commit()
    flash("The user is promoted to host member.", "info")
    return redirect(url_for("profiles.view_profile", id=id))


@admins.route("/pending-request")
@login_required
@is_admin
def pending_request():
    all_requests = PromotionPending.query.all()
    return render_template("admins/pending-request.html",
                           active="pending_request",
                           requests=all_requests,
                           total_requests=len(all_requests))


@admins.route("/pending-request/approve/<int:id>")
@login_required
@is_admin
def approve_pending_request(id: int):
    req_pending = PromotionPending.query.get(id)
    if not req_pending:
        flash("Promotion object not found!", "danger")
        return redirect(url_for("admins.pending_request"))
    req_pending.approved()
    # push notification
    notification = Notification(
        NotificationMessage.approvedPromotion(), url_for("events.create_event"), req_pending.profile.id)
    db.session.add(notification)
    db.session.commit()
    flash("Profile approved.", "info")
    return redirect(url_for("admins.pending_request"))


@admins.route("/pending-request/decline/<int:id>")
@login_required
@is_admin
def decline_pending_request(id: int):
    req_pending = PromotionPending.query.get(id)
    if not req_pending:
        flash("Promotion object not found!", "danger")
        return redirect(url_for("admins.pending_request"))
    db.session.delete(req_pending)
    # push notification
    notification = Notification(
        NotificationMessage.declinedPromotion(), "", req_pending.profile.id)
    db.session.add(notification)
    db.session.commit()
    flash("Profile declined.", "info")
    return redirect(url_for("admins.pending_request"))


@admins.route("/complain-box")
@login_required
@is_admin
def complain_box():
    complains = Complain.query.order_by(desc(Complain.created_at)).all()
    ban_form = BanUserForm()
    return render_template("admins/complain-box.html",
                           active="complain_box", len=len,
                           complains=complains, ban_form=ban_form)


@admins.route("/log")
@login_required
@is_admin
def log():
    return render_template("admins/log.html", active="log")


@admins.route("/banned-users")
@login_required
@is_admin
def banned_users():
    acc_restrictions = AccountRestriction.query.all()
    total_acc_restriction = len(acc_restrictions)
    return render_template("admins/banned-users.html",
                           active="banned_users",
                           acc_restrictions=acc_restrictions,
                           total_acc_restriction=total_acc_restriction)


@admins.route("/get-profiles-by-profile-id", methods=["POST"])
@login_required
@is_admin
def get_profile_by_profile_id():
    pid = request.form.get("get_by_profile_id")
    return redirect(url_for("profiles.view_profile", id=pid))


@admins.route("/get-profiles-by-user-id", methods=["POST"])
@login_required
@is_admin
def get_profile_by_user_id():
    uid = request.form.get("get_by_user_id")
    user = User.query.get(uid)
    if not user:
        return render_template("mains/errors.html", status=404, message="Profile not found!!")
    return redirect(url_for("profiles.view_profile", id=user.profile.id))


@admins.route("/get-profiles-by-email-id", methods=["POST"])
@login_required
@is_admin
def get_profile_by_email_id():
    email = request.form.get("get_by_email_id")
    user = User.query.filter_by(email=email).first()
    if not user:
        return render_template("mains/errors.html", status=404, message="Profile not found!!")
    return redirect(url_for("profiles.view_profile", id=user.profile.id))


@admins.route("/get-profiles-by-nid-id", methods=["POST"])
@login_required
@is_admin
def get_profile_by_nid_id():
    nid = request.form.get("get_by_nid_id")
    profile = Profile.query.filter_by(nid_number=nid).first()
    if not profile:
        return render_template("mains/errors.html", status=404, message="Profile not found!!")
    return redirect(url_for("profiles.view_profile", id=profile.id))


@admins.route("/unban/<int:id>")
@login_required
@is_admin
def unban_user(id: int):
    user = User.query.get(id)
    acc_restriction = user.profile.banned
    if not acc_restriction:
        flash("User is not banned.", "danger")
    else:
        db.session.delete(acc_restriction)
        # push notification
        notification = Notification(
            NotificationMessage.unban_user(), url_for("mains.homepage"), id)
        db.session.add(notification)
        db.session.commit()
        flash(f"The user is unbanned", "success")
    return redirect(url_for("profiles.view_profile", id=id))


@ admins.route("/ban/<int:id>", methods=["POST"])
@login_required
@is_admin
def ban_user(id: int):
    __ban_user(request.form, id)
    return redirect(url_for("profiles.view_profile", id=id))


@admins.route("/ban-and-resolve/<int:id>", methods=["POST"])
@login_required
@is_admin
def ban_user_and_close_complain(id: int):
    complain = Complain.query.get(id)
    if not complain:
        flash("Complain object not found!", "danger")
        return redirect(url_for('admins.complain_box'))
    banned_profile = __ban_user(request.form, complain.complain_for)
    if banned_profile:
        complains_against_banned_profile = Complain.query.filter_by(
            complain_for=banned_profile.id).all()
        notification = Notification(
            NotificationMessage.complain_resolved_by_ban(
                complain.get_complain_for().get_fullname()), "",
            complain.complained_by.id)
        for c in complains_against_banned_profile:
            n = Notification(
                NotificationMessage.user_banned_by_other_report(
                    c.get_complain_for().get_fullname()), "",
                c.complained_by.id)
            db.session.delete(c)
            db.session.add(n)
        db.session.delete(complain)
        db.session.add(notification)
        db.session.commit()
        flash("User banned successfully.", "success")
    return redirect(url_for("admins.complain_box"))


@admins.route("/warn/<int:id>")
@login_required
@is_admin
def warn_user(id: int):
    complain = Complain.query.get(id)
    if not complain:
        flash("Complain object not found!", "danger")
        return redirect(url_for('admins.complain_box'))
    notification_for_victim = Notification(
        NotificationMessage.complain_resolved_by_warning(
            complain.get_complain_for().get_fullname()), "",
        complain.complained_by.id)
    notification_for_reported_profile = Notification(
        NotificationMessage.warn_user(
            "You were reported by other user. Please be kind otherwise we will take action against you next time."), "",
        complain.get_complain_for().id)
    db.session.delete(complain)
    db.session.add(notification_for_victim)
    db.session.add(notification_for_reported_profile)
    db.session.commit()
    flash("Warned the user successfully.", "success")
    return redirect(url_for("admins.complain_box"))


@admins.route("/not-acceptable-report/<int:id>")
@login_required
@is_admin
def not_acceptable_report(id: int):
    complain = Complain.query.get(id)
    if not complain:
        flash("Complain object not found!", "danger")
        return redirect(url_for('admins.complain_box'))
    notification = Notification(
        NotificationMessage.complain_not_acceptable(
            complain.get_complain_for().get_fullname()), "",
        complain.complained_by.id)
    db.session.delete(complain)
    db.session.add(notification)
    db.session.commit()
    flash("Complain resolved successfully.", "success")
    return redirect(url_for("admins.complain_box"))
