"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, DEFAULT_IMAGE_URL, Post

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

# app.debug = True
app.config["SECRET_KEY"] = "oh-so-secret"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.get("/")
def homepage():
    """Redirects to list of users in database."""

    return redirect("/users")


@app.get("/users")
def list_users():
    """Populates page with list of all users in database."""

    users = User.query.all()

    return render_template("user-list.html", users=users)


@app.get("/users/new")
def add_users_form():
    """Shows a form to add a new user."""

    return render_template("user-add.html")


@app.post("/users/new")
def add_users():
    """Grabs information from form and submits new user to database
    and redirects to users list.
    """

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"] or None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.get("/users/<int:user_id>")
def show_user(user_id):
    """Shows detailed information about a specific user."""

    user = User.query.get_or_404(user_id)
    posts = user.posts

    return render_template("user-details.html", user=user, posts=posts)


@app.get("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Shows edit form for a specific user."""

    user = User.query.get_or_404(user_id)
    return render_template("user-edit.html", user=user)


@app.post("/users/<int:user_id>/edit")
def update_user(user_id):
    """Grabs information from form and updates the current user's information
    in the database, then redirects to users list.
    """

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form.get("image-url", DEFAULT_IMAGE_URL)

    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Deletes the current user from the database and redirects to the users list."""
    User.query.filter(User.id == user_id).delete()
    db.session.commit()
    return redirect("/users")


@app.get("/users/<int:user_id>/posts/new")
def new_post(user_id):
    """Displays form for user to add a new post"""

    user = User.query.get_or_404(user_id)

    return render_template("post-new.html", user=user)


@app.post("/users/<int:user_id>/posts/new")
def add_post(user_id):
    """Adds new post for current user id"""

    title = request.form["title"]
    content = request.form["content"]

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.get("/posts/<int:post_id>")
def show_post(post_id):
    """Shows a specific post."""

    post = Post.query.get_or_404(post_id)

    return render_template("post-details.html", post=post)


@app.get("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Shows edit form for a specific post."""

    post = Post.query.get_or_404(post_id)
    return render_template("post-edit.html", post=post)


@app.post("/posts/<int:post_id>/edit")
def update_post(post_id):
    """Grabs information from form and updates the current post's information
    in the database, then redirects to the associated user's posts list.
    """

    title = request.form["title"]
    content = request.form["content"]

    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.post("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Deletes the current post from the database and redirects to the page
    of the user associated with the current post.
    """
    post = Post.query.get_or_404(post_id)
    user_id = post.users.id
    Post.query.filter(Post.id == post_id).delete()
    db.session.commit()
    return redirect(f"/users/{user_id}")
