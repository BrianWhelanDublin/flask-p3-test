import os
from flask import (Flask, flash, render_template,
                   redirect, request, session,
                   url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (DataRequired,
                                Length, Email,
                                EqualTo,
                                ValidationError)
from flask_bcrypt import Bcrypt
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)
bcrypt = Bcrypt(app)


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
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "admin" and form.password.data == "12345":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful please check user details", "error")
    return render_template("login.html",
                           title="Login", form=form)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
