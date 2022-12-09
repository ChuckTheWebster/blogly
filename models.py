from flask_sqlalchemy import SQLAlchemy

# import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://scontent-lga3-1.xx.fbcdn.net/v/t1.6435-9/41353875_238097000189493_5943158895600992256_n.jpg?stp=cp0_dst-jpg_e15_p320x320_q65&_nc_cat=104&ccb=1-7&_nc_sid=85a577&_nc_ohc=86V_N6hIqsgAX_375Mx&_nc_ht=scontent-lga3-1.xx&oh=00_AfAz3pYHyM2VZBKZVknRA8l4gFZpaHV2TEbLwy5cisbDmQ&oe=63B877D9"


def connect_db(app):
    """Connect to the database."""
    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User class for users table in database."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    image_url = db.Column(db.Text, nullable=True, default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post")


class Post(db.Model):
    """Post class for posts table in database"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=db.func.now()
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    users = db.relationship("User")
