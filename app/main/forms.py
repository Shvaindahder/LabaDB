from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class AddNewDepForm(FlaskForm):
    head_of = StringField("Head Of", validators=[DataRequired()])
    password = PasswordField("Head Of password") # If empty -> User is exists
    address = StringField("Address", validators=[DataRequired()])
    submit = SubmitField("Добавить")