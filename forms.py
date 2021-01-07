from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (DataRequired,
                                Length, Email,
                                EqualTo,
                                ValidationError)


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


# class User:
#     def __init__(self, username):
#         self.username = username

#     @staticmethod
#     def is_authenticated():
#         return True

#     @staticmethod
#     def is_active():
#         return True

#     @staticmethod
#     def is_anonymous():
#         return False

#     def get_id(self):
#         return self.username

#     @login_manager.user_loader
#     def load_user(username):
#         u = mongo.db.users.find_one({"username": username})
#         if not u:
#             return None
#         return User(username=u['username'])