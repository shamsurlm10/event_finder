from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search = StringField("Search", validators=[
        DataRequired()
    ], render_kw={"placeholder": "search..."})
    submit = SubmitField("Search")

