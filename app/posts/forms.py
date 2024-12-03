from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.choices import SelectField, SelectMultipleField
from wtforms.fields.datetime import DateTimeLocalField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, Length

from app.posts.models import Tag
from app.users.models import User

CATEGORIES = [
    ('tech', 'Tech'),
    ('science', 'Science'),
    ('lifestyle', 'Lifestyle')
]

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2)])
    content = TextAreaField("Content", render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    is_active = BooleanField("Active")
    publish_date = DateTimeLocalField("Publish Date", format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    category = SelectField("Category", choices=CATEGORIES)
    author_id = SelectField("Author", coerce=int)
    tags = SelectMultipleField("Tags", coerce=int)
    submit = SubmitField("Add Post")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Завантаження списку авторів із БД
        self.author_id.choices = [(user.id, user.username) for user in User.query.all()]
        # Завантаження списку тегів із БД для SelectMultipleField
        self.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]