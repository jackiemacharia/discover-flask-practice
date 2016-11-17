
import unittest

from flask_login import current_user
from flask import request

from base import BaseTestCase
from project import bcrypt
from project.models import User


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

    # Ensure user can register
    def test_user_registration(self):
        with self.client:
            response = self.client.post(
                '/register', data=dict(username='jax', email='jax@example.com', password='password', confirm='password'),
                follow_redirects=True
            )
            self.assertIn(b'Welcome to Flask!', response.data)
            self.assertTrue(current_user.name == 'jax')
            self.assertTrue(current_user.is_active())
            user = User.query.filter_by(email='jax@example.com').first()
            self.assertTrue(str(user) == "<name - jax>")

    # Ensure errors are thrown during an incorrect user registration
    def test_incorrect_user_registeration(self):
        with self.client:
            response = self.client.post('/register', data=dict(
                username='Michael', email='michael',
                password='python', confirm='python'
            ), follow_redirects=True)
            self.assertIn(b'Invalid email address.', response.data)
            self.assertIn(b'/register', request.url)

    # Ensure registration errors are caught
    def test_registration_errors(self):
        with self.client:
            response = self.client.post(
                '/register', data=dict(username='jax', email='jax@example.com', password='password', confirm='pssword'),
                follow_redirects=True
            )
            self.assertIn(b'Invalid credentials. Please try again.', response.data)
            self.assertFalse(current_user.is_active)

    # Ensure id is correct for the current/logged in user
    def test_get_by_id(self):
            with self.client:
                self.client.post('/login', data=dict(
                    username="admin", password='admin'
                ), follow_redirects=True)
                self.assertTrue(current_user.id == 1)
                self.assertFalse(current_user.id == 20)

    def test_check_password(self):
        # Ensure given password is correct after unhashing
        user = User.query.filter_by(email='ad@min.com').first()
        self.assertTrue(bcrypt.check_password_hash(user.password, 'admin'))
        self.assertFalse(bcrypt.check_password_hash(user.password, 'foobar'))


if __name__ == '__main__':
    unittest.main()
