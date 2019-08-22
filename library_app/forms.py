from flask_wtf import FlaskForm
from wtforms import (
    PasswordField, SubmitField, StringField, PasswordField,
    BooleanField, SelectField, TextAreaField, IntegerField)
from wtforms.validators import Required, Length, Email

class LoginForm(FlaskForm):
    login_email = StringField(
        'E-mail address', validators=[Required(), Email()])
    login_password = PasswordField(
        'Password', validators=[Required(), Length(6)])
    remember_me = BooleanField('Remember?')
    login_submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    fullname = StringField('Full name')
    username = StringField(
        'Username', validators=[Required(), Length(6)])
    email = StringField(
        'E-mail address', validators=[Required(), Email()])
    phone = StringField('Phone Number', validators=[Required()])
    password = PasswordField(
        'Password', validators=[Required(), Length(8)])
    register_submit = SubmitField('Create account')


class BookForm(FlaskForm):
    title = StringField('Book title', validators=[Required()])
    edition = StringField('Edition', validators=[Required()])
    year = StringField('Year of publishing', validators=[Required()])
    price = StringField('Price')
    isbn = StringField('ISBN', validators=[Required()])
    pages = IntegerField('Number of pages')
    copies = IntegerField(
        'Number of copies available', validators=[Required()])
    description = TextAreaField('Description')
    author = SelectField()
    submit = SubmitField('Add Book')


# class AuthorForm(FlaskForm):
#     name = StringField('Author name', validators=[Required()])
#     email = StringField('Author email', validators=[Required(), Email()])
#     submit = SubmitField('Add Author')
