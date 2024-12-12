from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo, ValidationError

from app.users.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=4, max=50),
            Regexp(r"^\w+$", message="Username must contain only letters, numbers, or underscores.")
        ]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Invalid email address.")
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long.")
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match.")
        ]
    )
    submit = SubmitField("Register")

    # noinspection PyMethodMayBeStatic
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is already registered.")

    # noinspection PyMethodMayBeStatic
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is already taken.")