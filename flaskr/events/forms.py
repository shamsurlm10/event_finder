from datetime import datetime

from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (DateTimeLocalField, IntegerField, StringField,
                     SubmitField, TextAreaField, FileField)
from wtforms.validators import (URL, DataRequired, Length, Optional,
                                ValidationError)


class EventForm(FlaskForm):
    event_title = StringField("Event Title*", validators=[
        DataRequired(), Length(max=150, min=2)
    ], render_kw={"placeholder": "Enter a title of the event."})
    event_location = StringField("Event Location*", validators=[
        DataRequired(), Length(max=100, min=2)
    ], render_kw={"placeholder": "ex. City, Country."})
    event_start_time = DateTimeLocalField(
        "Event Start Time*", format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    event_max_members = IntegerField("Maximum Members*", validators=[DataRequired()],
                                     render_kw={"placeholder": "Enter the maximum number."})
    event_description = TextAreaField("Description*", validators=[DataRequired()],
                                      render_kw={"placeholder": "Tell about the event."})
    event_fee = IntegerField("Event Fee*", validators=[DataRequired()],
                             render_kw={"placeholder": "Enter the event fee (In Taka)."})
    event_days_count = IntegerField(
        "Number of days*", render_kw={"placeholder": "Event days."})
    event_nights_count = IntegerField(
        "Number of nights*", render_kw={"placeholder": "Event nights."})
    phone_number = StringField("Phone Number", validators=[DataRequired()],
                             render_kw={
                                 "placeholder": "Enter your phone number."
                             })
    hotel_name = StringField("Hotel Name",
                             render_kw={
                                 "placeholder": "Enter the name of hotel if the \event includes it."
                             })
    hotel_web_link = StringField("Hotel web link", validators=[Optional(), URL()],
                                 render_kw={
        "placeholder": "Enter the link of hotel. Such as facebook page link, booking.com link etc."
    })
    event_cover_photo = FileField("Event Cover Photo", validators=[
                                  FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("Submit")

    def validate_hotel_web_link(self, hotel_web_link):
        if not self.hotel_name.data and hotel_web_link.data:
            raise ValidationError(
                "Cannot set the weblink if hotel name field is remains empty.")

    def validate_event_start_time(self, event_start_time):
        current_date = datetime.utcnow()
        if current_date > event_start_time.data:
            raise ValidationError("Event start date cannot be in past.")

    def validate_event_fee(self, event_fee):
        if event_fee.data and event_fee.data < 0:
            raise ValidationError("Event fee can not be a negative value.")

    def validate_event_days_count(self, event_days_count):
        if event_days_count.data and event_days_count.data < 0:
            raise ValidationError(
                "Event days count can not be a negative value.")

    def validate_event_nights_count(self, event_nights_count):
        if event_nights_count.data and event_nights_count.data < 0:
            raise ValidationError(
                "Event nights count can not be a negative value.")
