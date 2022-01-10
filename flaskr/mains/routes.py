from flask import Blueprint, render_template, url_for
from flask.helpers import flash
from flask_login import current_user
from flaskr import app
from flaskr.mains.form import SearchForm
from flaskr.models import Event, Profile
from flaskr.utils import is_eligable
from sqlalchemy import func
from werkzeug.utils import redirect

mains = Blueprint("mains", __name__)


@mains.route("/homepage")
@mains.route("/")
def homepage():
    eligable = is_eligable(current_user)
    events = Event.query.order_by(Event.event_time)[:12]
    return render_template("mains/homepage.html", eligable=eligable, events=events, len=len)

@app.context_processor
def base():
    form = SearchForm()
    return dict(s_form=form)

@mains.route("/search", methods=["GET", "POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        searched = form.search.data
        events_by_title = Event.query.filter(func.lower(Event.title).like("%" + searched.lower() + "%"))
        events_by_location = Event.query.filter(func.lower(Event.place_name).like("%" + searched.lower() + "%"))
        
        event_set = set()
        for event in events_by_title:
            event_set.add(event)
        for event in events_by_location:
            event_set.add(event)
        
        profiles_by_first = Profile.query.filter(func.lower(Profile.first_name).like("%" + searched.lower() + "%"))
        profiles_by_last = Profile.query.filter(func.lower(Profile.last_name).like("%" + searched.lower() + "%"))
        
        profile_set = set()
        for profile in profiles_by_first:
            profile_set.add(profile)
        for profile in profiles_by_last:
            profile_set.add(profile)
        
        return render_template("mains/search.html", s_form=form, searched=searched, events=event_set, profiles=profile_set, len=len)
    flash("No search input given.", "danger")
    return redirect(url_for("mains.homepage"))
    
