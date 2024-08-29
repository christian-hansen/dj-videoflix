from django.test import TestCase, Client
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token  # Import Token model
# from django.contrib.auth.models import User
from users.models import CustomUser
from users.serializers import UserItemSerializer
from rest_framework import status

# Create your tests here.
class LoginTest(TestCase):
    # Tests for login functionality

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='test_user', password='test_password', email='test@example.com')

    def test_login_success(self):
        # Test successful login
        response = self.client.post(
            '/api/v1/login/', {'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)
        self.assertTrue('user_id' in response.data)
        self.assertTrue('email' in response.data)

    def test_login_failure(self):
        # Test failed login with incorrect password
        response = self.client.post(
            '/api/v1/login/', {'username': 'test_user', 'password': 'wrong_password'})
        # Expecting 400 Bad Request for failed login
        self.assertEqual(response.status_code, 400)

        # Test failed login with non-existent user
        response = self.client.post(
            '/api/v1/login/', {'username': 'nonexistent_user', 'password': 'password'})
        self.assertEqual(response.status_code, 400)

    def test_login_missing_credentials(self):
        # Test login with missing credentials
        response = self.client.post(
            '/api/v1/login/', {'username': 'test_user'})
        # Expecting 400 Bad Request for missing password
        self.assertEqual(response.status_code, 400)

    def test_logout_view(self):
        response = self.client.get('/logout')
        # Check if the user is logged out
        self.assertFalse('_auth_user_id' in self.client.session)

class RegisterViewTest(TestCase):
    # Tests for registration

    def setUp(self):
        self.client = Client()

    def test_register_success(self):
        # Test successful registration
        response = self.client.post(
            '/api/v1/register/', {'username': 'new_user', 'email': 'new_user@example.com', 'first_name': 'first_name', 'last_name': 'last_name', 'password': 'new_password'})
        self.assertEqual(response.status_code, 201)
        # Check if user is created
        self.assertEqual(CustomUser.objects.filter(username='new_user').count(), 1)

    def test_register_existing_username(self):
        # Test registration with existing username
        CustomUser.objects.create_user(
            username='existing_user', email='existing@example.com', first_name='first_name', last_name='last_name', password='existing_password')
        response = self.client.post(
            '/api/v1/register/', {'username': 'existing_user', 'email': 'another@example.com', 'first_name': 'first_name', 'last_name': 'last_name', 'password': 'new_password'})
        # Expecting 400 Bad Request for existing username
        self.assertEqual(response.status_code, 400)

    def test_register_existing_email(self):
        # Test registration with existing email
        CustomUser.objects.create_user(
            username='another_user', email='existing@example.com', password='another_password')
        response = self.client.post(
            '/api/v1/register/', {'username': 'new_user', 'email': 'existing@example.com', 'password': 'new_password'})
        # Expecting 400 Bad Request for existing email
        self.assertEqual(response.status_code, 400)

    def test_register_missing_fields(self):
        # Test registration with missing fields
        response = self.client.post(
            '/api/v1/register/', {'username': 'new_user', 'email': 'new_user@example.com'})
        # Expecting 400 Bad Request for missing password
        self.assertEqual(response.status_code, 400)