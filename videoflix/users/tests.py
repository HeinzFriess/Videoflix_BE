from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class LoginViewTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword', email_confirmed=True)
        self.client = APIClient()

    def test_successful_login(self):
        # Ensure a user can login successfully
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post('/path-to-login-view/', data, format='json')
        self.assertEqual(response.status_code, 202)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)

    def test_invalid_credentials(self):
        # Ensure login fails with invalid credentials
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post('/path-to-login-view/', data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Invalid credentials')

    def test_unconfirmed_email(self):
        # Create a user with unconfirmed email
        unconfirmed_user = User.objects.create_user(username='unconfirmed', email='unconfirmed@example.com', password='testpassword', email_confirmed=False)
        data = {'username': 'unconfirmed', 'password': 'testpassword'}
        response = self.client.post('/path-to-login-view/', data, format='json')
        self.assertEqual(response.status_code, 403)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Email address not validated')

    # Add more test cases for edge cases, different scenarios, etc.
