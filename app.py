"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, DEFAULT_IMAGE_URL

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
# debug toolbar
app.config["SECRET_KEY"] = "oh-so-secret"
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.get("/")
def homepage():

    return redirect("/users")


@app.get("/users")
def list_users():

    users = User.query.all()

    return render_template("user-list.html", users=users)


@app.get("/users/new")
def add_users_form():

    return render_template("user-add.html")


@app.post("/users/new")
def add_users():

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form.get("image-url")
    if image_url == "":
        image_url = DEFAULT_IMAGE_URL

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.get("/users/<int:user_id>")
def show_user(user_id):

    user = User.query.get_or_404(user_id)
    return render_template("user-details.html", user=user)


@app.get("/users/<int:user_id>/edit")
def edit_user(user_id):

    user = User.query.get_or_404(user_id)
    return render_template("user-edit.html", user=user)


@app.post("/users/<int:user_id>/edit")
def update_user(user_id):

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form.get("image-url", None)

    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    User.query.filter(User.id == user_id).delete()
    # user = User.query.get_or_404(user_id)
    # user.query.delete()
    db.session.commit()
    return redirect("/")
