from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class AuthUser(FlaskForm):
    username = StringField("name", validators=[DataRequired()], id="username-field")
    password = PasswordField("password", validators=[DataRequired()], id="password-field")
    submit = SubmitField("Далее")


