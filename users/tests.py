from django.test import TestCase, Client
from users.models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core import mail

# Create your tests here.
class LoginTest(TestCase):
    # Tests for login functionality

    def setUp(self):
        self.client = Client()
        self.active_user = CustomUser.objects.create_user(
            username='active_user', password='test_password', email='active@example.com', is_active=True)
        self.inactive_user = CustomUser.objects.create_user(
            username='inactive_user', password='test_password', email='inactive@example.com', is_active=False)

    def test_login_success(self):
        # Test successful login for an active user
        response = self.client.post(
            '/api/v1/login/', {'username': 'active_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)
        self.assertTrue('user_id' in response.data)
        self.assertTrue('email' in response.data)

    def test_login_inactive_user(self):
        # Test login for an inactive user
        response = self.client.post(
            '/api/v1/login/', {'username': 'inactive_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 403)  # Expecting 403 Forbidden
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'This account is inactive. Please activate your account.')

    def test_login_failure(self):
        # Test failed login with incorrect password
        response = self.client.post(
            '/api/v1/login/', {'username': 'active_user', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 400)

        # Test failed login with non-existent user
        response = self.client.post(
            '/api/v1/login/', {'username': 'nonexistent_user', 'password': 'password'})
        self.assertEqual(response.status_code, 400)

    def test_login_missing_credentials(self):
        # Test login with missing credentials
        response = self.client.post(
            '/api/v1/login/', {'username': 'active_user'})
        self.assertEqual(response.status_code, 400)

    def test_logout_view(self):
        # Assuming you have a logout view that handles token deletion
        response = self.client.get('/logout')
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
        user = CustomUser.objects.get(username='new_user')
        self.assertEqual(user.is_active, False)  # The user should be inactive

        # Check that an email has been sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Activate your Videoflix account', mail.outbox[0].subject)

    def test_register_existing_username(self):
        # Test registration with existing username
        CustomUser.objects.create_user(
            username='existing_user', email='existing@example.com', first_name='first_name', last_name='last_name', password='existing_password')
        response = self.client.post(
            '/api/v1/register/', {'username': 'existing_user', 'email': 'another@example.com', 'first_name': 'first_name', 'last_name': 'last_name', 'password': 'new_password'})
        self.assertEqual(response.status_code, 400)

    def test_register_existing_email(self):
        # Test registration with existing email
        CustomUser.objects.create_user(
            username='another_user', email='existing@example.com', password='another_password')
        response = self.client.post(
            '/api/v1/register/', {'username': 'new_user', 'email': 'existing@example.com', 'password': 'new_password'})
        self.assertEqual(response.status_code, 400)

    def test_register_missing_fields(self):
        # Test registration with missing fields
        response = self.client.post(
            '/api/v1/register/', {'username': 'new_user', 'email': 'new_user@example.com'})
        self.assertEqual(response.status_code, 400)

    def test_account_activation(self):
        # Test activating a newly registered account
        user = CustomUser.objects.create_user(
            username='inactive_user', email='inactive@example.com', password='password', is_active=False)
        
        # Generate the token and uidb64 for the user
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Simulate clicking the activation link
        response = self.client.get(f'/api/v1/activate/{uidb64}/{token}/')
        self.assertEqual(response.status_code, 200)

        # Refresh user from DB and check if activated
        user.refresh_from_db()
        self.assertTrue(user.is_active)  # User should now be active

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
        
        # Check if an email has been sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Videoflix Password Reset Request', mail.outbox[0].subject)
        
        # Extract the email content
        email_body = mail.outbox[0].body
        
        # Ensure the reset token is generated
        user = CustomUser.objects.get(email='test@example.com')
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Verify the uidb64 and token are in the email body
        self.assertIn(uidb64, email_body)
        self.assertIn(token, email_body)
        
        # TODO Update with final link
        # #Ensure the link to reset password contains the correct uidb64 and token
        reset_link = f"http://your-frontend-domain.com/reset-password/{uidb64}/{token}/"
        self.assertIn(reset_link, email_body)

    def test_password_reset_invalid_email(self):
        """Test password reset request with an invalid email."""
        
        response = self.client.post('/api/v1/password-reset/', {'email': 'invalid@example.com'})
        
        # Expecting 404 Not Found for non-existent email
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