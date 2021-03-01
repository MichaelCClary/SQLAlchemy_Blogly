from unittest import TestCase

from app import app
from models import db, User, default_url, Post
from datetime import datetime

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class BloglyTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample pet."""

        User.query.delete()

        user = User(first_name="FirstName", last_name="LastName")

        db.session.add(user)
        db.session.commit()

        post = Post(title="TestTitle", content="TestContent", user_id=user.id)

        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id
        self.user = user
        self.post = post

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
            self.assertIn(
                f"""<li><a href="/users/{self.user_id+1}">John Wayne</a></li>""", html)

    def test_edit_user(self):
        with app.test_client() as client:
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

    def test_view_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestTitle</h1>', html)

    def test_add_post(self):
        with app.test_client() as client:
            new_post = {"title": "TestTitle2",
                        "content": "TestContent2", "user_id": self.user_id}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=new_post,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li>TestTitle2</li>', html)

    def test_edit_post(self):
        with app.test_client() as client:
            edit_post = {"title": "Blah Blah",
                         "content": "Blah Blah Blah"}
            resp = client.post(f"/posts/{self.post_id}/edit", data=edit_post,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            test_post = Post.query.get(self.post_id)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(test_post.title, "Blah Blah")
            self.assertIn("<h1>Blah Blah</h1>", html)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(
                f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            test_post = Post.query.get(self.post_id)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("<h1>TestTitle</h1>", html)
