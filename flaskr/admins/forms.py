from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class BanUserForm(FlaskForm):
    reason = StringField("Reason", validators=[
        DataRequired()
    ], render_kw={"placeholder": "Tell the reason for this ban"})
    days = SelectField('Account Restriction Duration', choices=[(
        None, 'Enter how many days of restriction'), (1, 1), (3, 3), (7, 7), (14, 14), (365, 365)])
    submit = SubmitField("Ban User")
