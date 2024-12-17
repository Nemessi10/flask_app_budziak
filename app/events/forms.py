from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length
from app.events.models import EventCategory

class SportEventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateTimeField('Event Date', validators=[DataRequired()], format='%d.%m.%Y')
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Event')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_id.choices = [(c.id, c.name) for c in EventCategory.query.all()]
