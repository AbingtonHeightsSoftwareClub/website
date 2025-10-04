from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
import sqlalchemy as sa
from app import db
from models import Player


# In Flask, you can create forms using Python instead of HTML.

class LoginForm(FlaskForm):
    """
    Inherits from FlaskForm to build boilerplate code

    Takes in a username that is a string and must be filled out.

    Password is still a string, but it tells the browser/password manager that
    it is a password for autofill

    Remember me stores cookies (actually local storage for more modern websites)
    to identify users and autofill their credentials in. Their credentials are stored
    locally.
    """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    """
    Inherits from FlaskForm to build boilerplate code

    Takes in a username that is a string and must be filled out.

    Password is still a string, but it tells the browser/password manager that
    it is a password for autofill

    Second password confirms user knows the password
    """
    username = StringField("Username", validators=[DataRequired(), Length(min=1, max=30)])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username: StringField) -> None:
        # Looks through the database and makes sure no other players have the same username.
        player = db.session.scalar(sa.select(Player).where(Player.title == username.data))
        if player is not None:
            # The error is automatically handled by FlaskForm, and it puts the error
            # in little red text below the box.
            raise ValidationError("Please use a different username.")

