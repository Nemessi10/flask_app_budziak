from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, Length

CATEGORIES = [
    ('tech', 'Tech'),
    ('science', 'Science'),
    ('lifestyle', 'Lifestyle')
]

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2)])
    content = TextAreaField("Content", render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    is_active = BooleanField("Active")
    publish_date = DateField("Publish Date", format='%Y-%m-%d')
    category = SelectField("Category", choices=CATEGORIES)
    submit = SubmitField("Add Post")