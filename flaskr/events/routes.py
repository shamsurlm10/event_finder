from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flaskr import db
from flaskr.decorators import is_host, is_verified
from flaskr.events.forms import *
from flaskr.models import (Decline, Event, Notification, PaymentPending, Post,
                           Profile)
from flaskr.notifications.utils import NotificationMessage
from flaskr.profiles.utils import remove_photo, save_photos
from sqlalchemy import desc

events = Blueprint("events", __name__, url_prefix="/events")


@events.route("/")
def get_events():
    all_events = Event.query.order_by(desc(Event.created_at)).all()
    return render_template("events/events.html", events=all_events, len=len)


@events.route("/<int:id>")
def view_event(id: int):
    event = Event.query.get(id)
    if not event:
        return render_template("mains/errors.html", status=404, message="Event not found!")
    query_str = request.args.get("filter")
    members_sub_query = request.args.get("members")
    recive_number = event.phone_number or "01xxxxxxxxx"

    if query_str == "messages":
        return render_template("events/view-event/messages.html",
                               len=len, str=str, event=event,
                               active='messages', recive_number=recive_number)
    if query_str == "members":
        sub_menu = "members"
        if members_sub_query == "pending":
            sub_menu = "pending-members"
        elif members_sub_query == "decline":
            sub_menu = "decline-members"
        return render_template("events/view-event/members.html",
                               len=len, str=str, event=event,
                               active="members", sub_menu=sub_menu,
                               recive_number=recive_number)
    if query_str == "posts":
        posts = Post.query.filter_by(event_id=id).order_by(desc(Post.created_at)).all()
        return render_template("events/view-event/posts.html",
                               len=len, str=str, event=event,
                               active='posts', recive_number=recive_number,
                               posts=posts)
    # if none of the avobe is true
    return render_template("events/view-event/details.html",
                           len=len, str=str, event=event,
                           active='details', recive_number=recive_number)


@events.route("/create", methods=["GET", "POST"])
@login_required
@is_verified
@is_host
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(form.event_title.data, form.event_description.data, form.event_location.data,
                      form.event_start_time.data, form.event_days_count.data, form.event_nights_count.data,
                      form.event_fee.data, current_user.profile.id, form.event_cover_photo.data,
                      form.event_max_members.data, form.hotel_name.data, form.hotel_web_link.data, form.phone_number.data)
        if form.event_cover_photo.data:
            # saving
            photo_file = save_photos(
                form.event_cover_photo.data, event.id, "eventCover", 1180, 450)
            event.cover_photo = "/images/uploads/eventCover/" + photo_file
        db.session.add(event)
        db.session.commit()
        current_user.profile.add_joined_events(event.id)
        flash(f"Event information saved", "success")
        return redirect(url_for("events.view_event", id=event.id))
    return render_template("events/create-event.html", form=form)


@events.route("/settings/info/<int:id>", methods=["GET", "POST"])
@login_required
def event_info(id: int):
    event = Event.query.get(id)
    if not event:
        return render_template("mains/errors.html", status=404, message="Event not found!")
    if event.host.id != current_user.profile.id:
        flash("Only the host can access this route", "danger")
        return redirect(url_for("events.view_event", id=event.id))
    form = EventForm()
    if request.method == "POST":
        # post request
        event.title = form.event_title.data
        event.description = form.event_description.data
        event.place_name = form.event_location.data
        event.event_time = form.event_start_time.data
        event.day = form.event_days_count.data
        event.night = form.event_nights_count.data
        event.fee = form.event_fee.data
        event.hotel_name = form.hotel_name.data
        event.hotel_weblink = form.hotel_web_link.data
        event.phone_number = form.phone_number.data
        if form.event_cover_photo.data:
            file_path = event.cover_photo
            if not ("/images/default/CoverPhotos/event-default.png" in file_path):
                remove_photo(file_path)
            # saving
            photo_file = save_photos(
                form.event_cover_photo.data, event.id, "eventCover", 1180, 450)
            event.cover_photo = "/images/uploads/eventCover/" + photo_file
        db.session.commit()
        flash(f"Event information saved", "success")
    # add the values
    elif request.method == "GET":
        form.event_title.data = event.title
        form.event_description.data = event.description
        form.event_location.data = event.place_name
        form.event_start_time.data = event.event_time
        form.event_days_count.data = event.day
        form.event_nights_count.data = event.night
        form.event_fee.data = event.fee
        form.hotel_name.data = event.hotel_name
        form.hotel_web_link.data = event.hotel_weblink
        form.phone_number.data = event.phone_number
    return render_template("events/event-info.html", active="event-info", form=form, event=event)


@events.route("/settings/plans/<int:id>", methods=["GET", "POST"])
@login_required
def event_plans(id: int):
    event = Event.query.get(id)
    if event.host.id != current_user.profile.id:
        flash("Only the host can access this route", "danger")
        return redirect(url_for("events.view_event", id=event.id))
    if request.method == "POST":
        list_of_plans = []
        for i in range(event.day+event.night):
            list_of_plans.append(request.form.get(f"event_plans_{i}"))
        event.plans = list_of_plans
        db.session.commit()
        flash("Event updated successfully.", "success")
    return render_template("events/edit-plans.html", active="event-plans", event=event)


@events.route("/upload/<int:id>", methods=["POST"])
@login_required
def add_photos(id: int):
    event = Event.query.get(id)
    if not event:
        return render_template("mains/errors.html", status=404, message="Event not found!")
    if event.host.id != current_user.profile.id:
        flash("Only the host can access this route", "danger")
        return redirect(url_for("events.view_event", id=event.id))
    photo_1 = request.files.get("photo_1")
    photo_2 = request.files.get("photo_2")
    photo_3 = request.files.get("photo_3")

    if photo_1:
        photo_file = save_photos(
            photo_1, event.id, "eventPhotos", 1280, 720)
        event.add_photo("/images/uploads/eventPhotos/" + photo_file)

    if photo_2:
        photo_file = save_photos(
            photo_2, event.id, "eventPhotos", 1280, 720)
        event.add_photo("/images/uploads/eventPhotos/" + photo_file)

    if photo_3:
        photo_file = save_photos(
            photo_3, event.id, "eventPhotos", 1280, 720)
        event.add_photo("/images/uploads/eventPhotos/" + photo_file)

    flash("Photos uploaded successfully.", "success")
    return redirect(url_for("events.view_event", id=event.id))


@events.route("/register/<int:id>", methods=["POST"])
@login_required
def register_for_event(id: int):
    trnx_id = request.form.get("trnx_id")
    event = Event.query.get(id)
    if not event:
        flash("Event not found!", "danger")
        return redirect(url_for("mains.homepage"))
    if not trnx_id:
        return redirect(url_for("events.view_event", id=id))
    if not event.event_status().get("status"):
        flash("Registration closed.", "danger")
        return redirect(url_for("events.view_event", id=id))
    pending = PaymentPending(trnx_id, current_user.profile.id, id)
    db.session.add(pending)
    notify = Notification(NotificationMessage.pending_payments(current_user.profile.get_fullname(
    )), url_for("events.view_event", id=id, filter="members", members="pending"), event.host.id)
    db.session.add(notify)
    db.session.commit()
    flash("Request successfully sent.", "success")
    return redirect(url_for("events.view_event", id=id))


@events.route("/<int:event_id>/accept/<int:profile_id>")
@login_required
def accept_pending_members(event_id: int, profile_id: int):
    event = Event.query.get(event_id)
    profile = Profile.query.get(profile_id)
    
    if not event:
        flash("Event not found!.", "danger")
        return redirect(url_for("events.view_event", id=event_id, filter="members", members="pending"))
    
    if not profile:
        flash("Profile not found!.", "danger")
        return redirect(url_for("events.view_event", id=event_id, filter="members", members="pending"))
    
    if current_user.profile.id != event.host.id:
        flash("You can not access the route.", "danger")
        return redirect(url_for("events.view_event", id=event_id, filter="members", members="pending"))
    pending_payments = event.pending_payments
    for i in pending_payments:
        if profile_id == i.profile.id:
            i.approve()
            if i.decline:
                i.decline.resolve()
            break
    event.add_members(profile_id)
    profile.add_joined_events(event.id)
    notification = Notification(NotificationMessage.approve_event_registration(),
                                url_for("events.view_event", id=event.id),
                                profile_id)
    db.session.add(notification)
    db.session.commit()
    flash("Member approved.", "info")
    return redirect(url_for("events.view_event", id=event_id, filter="members", members="pending"))


@events.route("/<int:event_id>/decline/<int:payment_id>", methods=["POST"])
@login_required
def decline_pending_members(event_id: int, payment_id: int):
    reason = request.form.get("reason")
    if not reason or reason == "":
        flash("First specify the reason.", "danger")
        return redirect(url_for("events.view_event", id=event_id, filter="members", members="pending"))
    event = Event.query.get(event_id)
    if not event:
        flash("Event not found!.", "danger")
        return redirect(url_for("events.view_event", id=event_id, filter="members", members="pending"))

    if current_user.profile.id != event.host.id:
        flash("You can not access the route.", "danger")
        return redirect(url_for("events.view_event", id=event_id, filter="members", members="pending"))

    pending_payments = event.pending_payments
    pending_payment = None
    for payment in pending_payments:
        if payment.id == payment_id:
            pending_payment = payment
    if not pending_payment:
        flash("User is not a member of this event.", "danger")
        return redirect(url_for("events.view_event", id=event_id, filter="members", members="pending"))

    decline = Decline(reason, payment_id)
    db.session.add(decline)
    notification = Notification(NotificationMessage.declin_event_registration(),
                                url_for("events.view_event", id=event.id),
                                pending_payment.profile.id)
    db.session.add(notification)
    db.session.commit()
    flash("Member declined.", "info")
    return redirect(url_for("events.view_event", id=event_id, filter="members", members="pending"))


@events.route("/make-registration-closed/<int:id>")
@login_required
def make_registration_close(id: int):
    event = Event.query.get(id)
    if not event:
        flash("Event not found!.", "danger")
        return redirect(url_for("events.view_event", id=id))

    if current_user.profile.id != event.host.id:
        flash("You can not access the route.", "danger")
        return redirect(url_for("events.view_event", id=id))
    
    event.is_open = False
    db.session.commit()
    flash("Event registration is now close.", "info")
    return redirect(url_for("events.view_event", id=id))
