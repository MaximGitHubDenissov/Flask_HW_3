from wtforms import StringField, PasswordField, EmailField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length, EqualTo, NoneOf


class RegistrationForm(FlaskForm):
    user_name = StringField('Имя', validators=[DataRequired()])
    user_last_name = StringField('Фамилия', validators=[DataRequired()])
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    user_password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6, max=12)])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('user_password')])


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6, max=12)])
