"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
# debug toolbar
app.config["SECRET_KEY"] = "oh-so-secret"
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.get('/')
def homepage():

    return redirect('/users')

@app.get('/users')
def list_users():

    users = User.query.all()

    return render_template("user-list.html", users=users)


@app.get('/users/new')
def add_users_form():

    return render_template('users-add.html')


@app.post('/users/new')
def add_users():

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form.get('image-url', None)

    user = User(first_name, last_name, image_url)

    db.session.add(user)
    db.session.commit()

    return render_template("")

@app.get('/users/<int:user-id>')
    def