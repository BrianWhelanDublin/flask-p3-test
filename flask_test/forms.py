from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (DataRequired,
                                Length, Email,
                                EqualTo,
                                ValidationError)
from flask_test import mongo


class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(),
                                                 EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = mongo.db.users.find_one(
            {"username": username.data.lower()}
        )
        if user:
            raise ValidationError("Username already exists")

    def validate_email(self, email):
        user = mongo.db.users.find_one(
             {"email": email.data}
        )
        if user:
            raise ValidationError("Email already exists")


class LoginForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = mongo.db.users.find_one(
                {"username": username.data.lower()}
            )
            if user:
                raise ValidationError("Username already exists")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = mongo.db.users.find_one(
                {"email": email.data}
            )
            if user:
                raise ValidationError("Email already exists")
