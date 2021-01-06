import os
from flask import (Flask, flash, render_template,
                   redirect, request, session,
                   url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import RegistrationForm, LoginForm
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
def home():
    return render_template("home.html", title="Home")


@app.route("/get_posts")
def get_posts():
    posts = mongo.db.posts.find()
    return render_template("posts.html",
                           title="Posts", posts=posts)


@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template("register.html",
                           title="Register", form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html",
                           title="Login", form=form)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
