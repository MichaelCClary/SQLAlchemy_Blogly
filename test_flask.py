from unittest import TestCase

from app import app
from models import db, User, default_url

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class PetViewsTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""

        User.query.delete()

        user = User(first_name="FirstName", last_name="LastName")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('FirstName', html)

    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>FirstName LastName</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            new_user = {"first_name": "John",
                        "last_name": "Wayne", "image_url": default_url}
            resp = client.post("/users/new", data=new_user,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/users/2">John Wayne</a></li>', html)

    def test_edit_user(self):
        with app.test_client() as client:
            print(self.user_id)
            edit_user = {"first_name": "Tarzan",
                         "last_name": "KingOfApes", "image_url": default_url}
            resp = client.post(f"/users/{self.user_id}/edit", data=edit_user,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            test_user = User.query.get(self.user_id)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(test_user.first_name, "Tarzan")
            self.assertEqual(test_user.last_name, "KingOfApes")
            self.assertIn(
                f"""<li><a href="/users/{self.user_id}">Tarzan KingOfApes</a></li>""", html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete",
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('FirstName', html)
