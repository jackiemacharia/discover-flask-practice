import unittest
from project import app, db
from flask_testing import TestCase
from project.models import User, BlogPost


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(BlogPost("Test post", "Hello from the other side"))
        db.session.add(User("admin", "ad@min.com", "admin"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that login page loads correctly
    def test_login_page_loads(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)

    # Ensure that login page behaves correctly given correct credentials
    def test_correct_login(self):
        response = self.client.post(
            '/login', data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'You were just logged in', response.data)

    # Ensure that login page behaves correctly given incorrect credentials
    def test_incorrect_login(self):
        response = self.client.post(
            '/login', data=dict(username="anhfkd", password="kfvf"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid credentials. Please try again.', response.data)

    # Ensure that logout page behaves correctly
    def test_logout(self):
        response = self.client.post(
            '/login', data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You were just logged out', response.data)

    # Ensure that main page requires login
    def test_main_route_requires_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    # Ensure that logout page requires user to be logged in first
    def test_logout_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You need to login first', response.data)

    # Ensure that posts show up on the main page

    def test_posts_show_up_on_main_page(self):
        response = self.client.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Hello from the other side', response.data)  # Never mix test data with real data


if __name__ == '__main__':
    unittest.main()
