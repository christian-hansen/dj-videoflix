from django.test import TestCase, Client
from users.models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

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
        


class PasswordResetTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='test_user', email='test@example.com', password='old_password')
        
    def test_password_reset_request(self):
        """Test if password reset request sends the reset link (token generation)."""
        
        response = self.client.post('/api/v1/password-reset/', {'email': 'test@example.com'})
        
        # Check if the response is OK (200)
        self.assertEqual(response.status_code, 200)
        
        # Ensure the reset token is generated
        user = CustomUser.objects.get(email='test@example.com')
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Simulate checking the token and uidb64 in email
        self.assertIsNotNone(token)
        self.assertIsNotNone(uidb64)

    def test_password_reset_invalid_email(self):
        """Test password reset request with an invalid email."""
        
        response = self.client.post('/api/v1/password-reset/', {'email': 'invalid@example.com'})
        
        # Expecting 400 Bad Request for non-existent email
        self.assertEqual(response.status_code, 404)
    
    def test_password_reset_confirm(self):
        """Test resetting the password using a valid token and setting a new password."""
        
        # Generate token and uidb64 for the user
        user = CustomUser.objects.get(email='test@example.com')
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Set new password using token and uidb64
        new_password_data = {
            'new_password': 'new_password123',
            'confirm_password': 'new_password123'
        }
        
        reset_url = f'/api/v1/reset-password/{uidb64}/{token}/'
        response = self.client.post(reset_url, new_password_data)
        
        # Ensure the password reset was successful
        self.assertEqual(response.status_code, 200)
        
        # Check if the user can log in with the new password
        login_response = self.client.post(
            '/api/v1/login/', {'username': 'test_user', 'password': 'new_password123'})
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue('token' in login_response.data)

    def test_password_reset_invalid_token(self):
        """Test password reset with an invalid token."""
        
        # Use an invalid token for the reset
        invalid_token = 'invalid-token'
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        
        new_password_data = {
            'new_password': 'new_password123',
            'confirm_password': 'new_password123'
        }
        
        reset_url = f'/api/v1/reset-password/{uidb64}/{invalid_token}/'
        response = self.client.post(reset_url, new_password_data)
        
        # Expecting 400 Bad Request for invalid token
        self.assertEqual(response.status_code, 400)
    
    def test_password_reset_mismatch_password(self):
        """Test password reset with mismatching new password and confirm password."""
        
        user = CustomUser.objects.get(email='test@example.com')
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Send mismatched passwords
        new_password_data = {
            'new_password': 'new_password123',
            'confirm_password': 'different_password'
        }
        
        reset_url = f'/api/v1/reset-password/{uidb64}/{token}/'
        response = self.client.post(reset_url, new_password_data)
        
        # Expecting 400 Bad Request for mismatching passwords
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.data)