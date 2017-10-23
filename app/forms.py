from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, InputRequired, EqualTo


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    # password = PasswordField('password', validators=[DataRequired()])
    password = PasswordField('password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    cpassword = PasswordField('confirm', validators=[DataRequired()])
