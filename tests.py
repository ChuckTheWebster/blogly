from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, connect_db

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

    # WORKING ONNNNN
    def test_user_list(self):
        with app.test_client as client:
            response = client.get('/users')
            html = response.get_(as_text=True)

            user = User.query.get(1)
            first_name = user.first_name
            last_name = user.last_name

            self.assert_Equal(response.status_code, 200)
            self.assertIn(f'{first_name} {last_name}', html)


    def test_user_add_form(self):
        with app.test_client() as client:
            response = client.get('/users/new')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<form', html)


    def test_user_add_submit(self):
        with app.test_client() as client:
            response = client.post('/users/new',
                                    data={'first_name': 'Foo',
                                    'last_name': 'Bar'}, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Foo', html)


    def test_user_edit_submit(self):
        with app.test_client() as client:
            response = client.post('/users/1',
                                    data={'first_name': 'Big',
                                    'last_name': 'Mike'}, follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Big', html)


    def test_redirection(self):
        with app.test_client as client:
            response = client.get('/')

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, "/users")


    def test_redirection_followed(self):
        with app.test_client() as client:
            response = client.get("/", follows_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<button', html)


    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test1_first", html)
            self.assertIn("test1_last", html)