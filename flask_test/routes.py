import os
from flask import (flash, render_template,
                   redirect, request,
                   url_for)
# from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, BooleanField
# from wtforms.validators import (DataRequired,
#                                 Length, Email,
#                                 EqualTo,
#                                 ValidationError)
# from flask_bcrypt import Bcrypt
from flask_test import app, bcrypt, mongo
from flask_test.forms import (RegistrationForm,
                              LoginForm,
                              UpdateAccountForm)
from flask_test.models import User
from flask_login import (current_user, login_user,
                         logout_user, login_required)
if os.path.exists("env.py"):
    import env


# app = Flask(__name__)


# app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
# app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


# mongo = PyMongo(app)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager(app)
# login_manager.login_view = "login"
# login_manager.login_message_category = "error"


# class RegistrationForm(FlaskForm):
#     username = StringField("Username",
#                            validators=[DataRequired(),
#                                        Length(min=2, max=20)])
#     email = StringField("Email",
#                         validators=[DataRequired(), Email()])
#     password = PasswordField("Password",
#                              validators=[DataRequired()])
#     confirm_password = PasswordField("Confirm Password",
#                                      validators=[DataRequired(),
#                                                  EqualTo("password")])
#     submit = SubmitField("Sign Up")

#     def validate_username(self, username):
#         user = mongo.db.users.find_one(
#             {"username": username.data.lower()}
#         )
#         if user:
#             raise ValidationError("Username already exists")

#     def validate_email(self, email):
#         user = mongo.db.users.find_one(
#              {"email": email.data}
#         )
#         if user:
#             raise ValidationError("Email already exists")


# class LoginForm(FlaskForm):
#     username = StringField("Username",
#                            validators=[DataRequired(),
#                                        Length(min=2, max=20)])
#     password = PasswordField("Password",
#                              validators=[DataRequired()])
#     remember = BooleanField("Remember Me")
#     submit = SubmitField("Login")


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


# @login_manager.user_loader
# def load_user(username):
#     user = mongo.db.users.find_one({"username": username})
#     if not user:
#         return None
#     return User(user["username"])


@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/get_posts")
def get_posts():
    posts = mongo.db.posts.find()
    return render_template("posts.html",
                           title="Posts", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = RegistrationForm()

    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")

        register_user = {
            "username": form.username.data.lower(),
            "email": form.email.data,
            "password": hashed_password,
            "posts": ""
        }

        mongo.db.users.insert_one(register_user)

        flash("Account created You may now login", "success")

        return redirect(url_for("login"))

    return render_template("register.html",
                           title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one(
            {"username": form.username.data})
        if user and bcrypt.check_password_hash(user["password"],
                                               form.password.data):
            user_obj = User(user)
            login_user(user_obj, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("User Logged In Sucessfully", "success")
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("home"))

        else:
            flash("Login Unsuccessful please check user details", "error")
    return render_template("login.html",
                           title="Login", form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash("Logged out")
    return redirect(url_for("login"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        mongo.db.users.update({"username": current_user.username},
                              {"$set": {
                                  "username": form.username.data,
                                  "email": form.email.data
                              }})
        flash("Your account has been updated", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html",
                           title="account",
                           form=form)


# if __name__ == "__main__":
#     app.run(host=os.environ.get("IP"),
#             port=os.environ.get("PORT"),
#             debug=True)
