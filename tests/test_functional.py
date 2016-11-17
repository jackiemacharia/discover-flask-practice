import unittest
from flask_login import current_user
from base import BaseTestCase


class FlaskTestCase(BaseTestCase):

    # Ensure that flask was set up correctly
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that main page requires login
    def test_main_route_requires_login(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'Please log in to access this page.', response.data)

    # Ensure that welcome page loads
    def test_welcome_route_works_as_expected(self):
        response = self.client.get('/welcome', follow_redirects=True)
        self.assertIn(b'Welcome to Flask!', response.data)

    # Ensure that posts show up on the main page
    def test_posts_show_up_on_main_page(self):
        response = self.client.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Hello from the other side', response.data)  # Never mix test data with real data


class UserViewsTests(BaseTestCase):
    # Ensure that login page loads correctly
    def test_login_page_loads(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)

    # Ensure that login page behaves correctly given correct credentials
    def test_correct_login(self):
        with self.client:
            response = self.client.post(
                '/login', data=dict(username="admin", password="admin"),
                follow_redirects=True
            )
            self.assertIn(b'You were just logged in', response.data)
            self.assertTrue(current_user.name == 'admin')
            self.assertTrue(current_user.is_active())

    # Ensure that login page behaves correctly given incorrect credentials
    def test_incorrect_login(self):
        response = self.client.post(
            '/login', data=dict(username="anhfkd", password="kfvf"),
            follow_redirects=True
        )
        self.assertIn(b'Invalid credentials. Please try again.', response.data)

    # Ensure that logout page behaves correctly
    def test_logout(self):
        with self.client:
            response = self.client.post(
                '/login', data=dict(username="admin", password="admin"),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You were just logged out', response.data)
            self.assertFalse(current_user.is_active)

    # Ensure that logout page requires user to be logged in first
    def test_logout_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please log in to access this page.', response.data)


if __name__ == '__main__':
    unittest.main()
