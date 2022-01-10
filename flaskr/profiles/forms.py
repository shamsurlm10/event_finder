from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from flaskr import bcrypt
from flaskr.models import User
from wtforms import (DateField, PasswordField, StringField, SubmitField,
                     TextAreaField)
from wtforms.validators import (URL, DataRequired, EqualTo, Length, Optional,
                                ValidationError)


class ProfileInfoForm(FlaskForm):
    bio = TextAreaField("Bio", validators=[Length(max=500)],  render_kw={
                        "placeholder": "Write your bio here..."})
    first_name = StringField("First Name", validators=[
        DataRequired(), Length(max=15, min=2)
    ], render_kw={"placeholder": "ex. Alen"})
    last_name = StringField("Last Name", validators=[
        DataRequired(), Length(max=15, min=2)
    ], render_kw={"placeholder": "ex. Walker"})
    dob = DateField("Date of Birth", validators=[
        DataRequired()
    ])
    nid = StringField("National Identity Card", validators=[
        Length(max=11)
    ], render_kw={"placeholder": "ex. 1234567890"})
    save = SubmitField("Update")


class VerifyEmailForm(FlaskForm):
    token = StringField("Verification Token", validators=[
        DataRequired(), Length(max=6)
    ], render_kw={"placeholder": "Enter your verification token here..."})
    save = SubmitField("Update")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[
        DataRequired(), Length(min=6)
    ], render_kw={"placeholder": "Type your old password"})

    new_password = PasswordField("New Password", validators=[
        DataRequired(), Length(min=6)
    ], render_kw={"placeholder": "Type a new password"})

    c_password = PasswordField("Confirm Password", validators=[
        DataRequired(), Length(min=6), EqualTo(
            "new_password", "Confirm password did not matched")
    ], render_kw={"placeholder": "Retype the password"})

    save = SubmitField("Update")

    def validate_old_password(self, old_password):
        user = User.query.get(current_user.id)
        if not bcrypt.check_password_hash(user.password, old_password.data):
            raise ValidationError("Password did not matched.")


class ChangePhoto(FlaskForm):
    cover_photo = FileField("Cover Photo", validators=[
                            FileAllowed(["jpg", "jpeg", "png"])])
    profile_photo = FileField("Profile Photo", validators=[
                              FileAllowed(["jpg", "jpeg", "png"])])
    save = SubmitField("Update")


class ChangeConnections(FlaskForm):
    facebook = StringField("Facebook", validators=[Optional(), URL()], render_kw={
                           "placeholder": "Facebook profile link"})
    twitter = StringField("Twitter", validators=[Optional(), URL()], render_kw={
                          "placeholder": "Twitter profile link"})
    github = StringField("Github", validators=[Optional(), URL()], render_kw={
                         "placeholder": "Github profile link"})
    linkedin = StringField("Linkedin", validators=[Optional(), URL()], render_kw={
                           "placeholder": "Linkedin profile link"})
    website = StringField("Website", validators=[Optional(), URL()], render_kw={
                          "placeholder": "Website link"})
    save = SubmitField("Update")
