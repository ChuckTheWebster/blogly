from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, connect_db, Post

# Let's configure our app to use a different database for tests
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

connect_db(app)

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test1_first",
            last_name="test1_last",
            image_url=None,
        )

        second_user = User(
            first_name="test2_first",
            last_name="test2_last",
            image_url=None,
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def test_user_list(self):
        """Tests if test user shows up on user list."""
        with self.client as client:
            response = client.get("/users")
            html = response.get_data(as_text=True)

            user = User.query.get(self.user_id)
            first_name = user.first_name
            last_name = user.last_name

            self.assertEqual(response.status_code, 200)
            self.assertIn(f"{first_name} {last_name}", html)

    def test_user_add_form(self):
        """Tests if new user form loads properly."""
        with self.client as client:
            response = client.get("/users/new")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<form", html)

    def test_user_add_submit(self):
        """Tests if submitting new dummy user updates users list."""
        with self.client as client:
            response = client.post(
                "/users/new",
                data={"first-name": "Foo", "last-name": "Bar"},
                follow_redirects=True,
            )
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Foo", html)

    def test_user_edit_submit(self):
        """Tests if editing test users reflect on the users list."""
        with self.client as client:
            response = client.post(
                f"/users/{self.user_id}/edit",
                data={
                    "first-name": "Big",
                    "last-name": "Mike",
                    "image-url": DEFAULT_IMAGE_URL,
                },
                follow_redirects=True,
            )
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Big Mike", html)

    def test_redirection(self):
        """Tests if redirections are working and rediction location is correct."""
        with self.client as client:
            response = client.get("/")

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, "/users")

    def test_redirection_followed(self):
        """Tests if redirections end up directing to a valid page."""
        with self.client as client:
            response = client.get("/", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<button", html)






    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    # def test_list_users(self):
    #     """Tests if the test users are in the users list."""
    #     with self.client as c:
    #         resp = c.get("/users")
    #         self.assertEqual(resp.status_code, 200)
    #         html = resp.get_data(as_text=True)
    #         self.assertIn("test1_first", html)
    #         self.assertIn("test1_last", html)

class PostViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()

        self.client = app.test_client()

        test_post = Post(
            title = "Chuck's Show",
            content = "Chuck is running this show",
            user_id = "1"
        )

        second_post = Post(
            title = "Pych, it's Ken's Show",
            content = "Ken is running this show",
            user_id = "2"
        )

        db.session.add_all([test_post, second_post])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.post_id = test_post.id


    def test_view_post(self):
        "Tests if posts show up on user's detail page"
        with self.client as client:
            response = client.get(f"/post/{self.post_id}")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Chuck's Show", html)

    def test_edit_post(self):
        """Test if post edits"""
        with self.client as client:
            response = client.post(
                f"/post/{self.post_id}/edit",
                data={'title'='Whatever', 'content'='Double Whatever'}, follow_redirects=True)

            html = response.get_data





     def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

        #Everything below this line gets deleted and is only for reference:

        #  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     title = db.Column(db.Text, nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     created_at = db.Column(
#         db.DateTime(timezone=True), nullable=False, default=db.func.now()
#     )
#     user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def test_user_list(self):
        """Tests if test user shows up on user list."""
        with self.client as client:
            response = client.get("/users")
            html = response.get_data(as_text=True)

            user = User.query.get(self.user_id)
            first_name = user.first_name
            last_name = user.last_name

            self.assertEqual(response.status_code, 200)
            self.assertIn(f"{first_name} {last_name}", html)

    def test_user_add_form(self):
        """Tests if new user form loads properly."""
        with self.client as client:
            response = client.get("/users/new")
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<form", html)

    def test_user_add_submit(self):
        """Tests if submitting new dummy user updates users list."""
        with self.client as client:
            response = client.post(
                "/users/new",
                data={"first-name": "Foo", "last-name": "Bar"},
                follow_redirects=True,
            )
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Foo", html)

    def test_user_edit_submit(self):
        """Tests if editing test users reflect on the users list."""
        with self.client as client:
            response = client.post(
                f"/users/{self.user_id}/edit",
                data={
                    "first-name": "Big",
                    "last-name": "Mike",
                    "image-url": DEFAULT_IMAGE_URL,
                },
                follow_redirects=True,
            )
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("Big Mike", html)

    def test_redirection(self):
        """Tests if redirections are working and rediction location is correct."""
        with self.client as client:
            response = client.get("/")

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, "/users")

    def test_redirection_followed(self):
        """Tests if redirections end up directing to a valid page."""
        with self.client as client:
            response = client.get("/", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn("<button", html)

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    # def test_list_users(self):
    #     """Tests if the test users are in the users list."""
    #     with self.client as c:
    #         resp = c.get("/users")
    #         self.assertEqual(resp.status_code, 200)
    #         html = resp.get_data(as_text=True)
    #         self.assertIn("test1_first", html)
    #         self.assertIn("test1_last", html)
