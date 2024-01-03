from django.test import TestCase

# Create your tests here.

from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Video

class VideoViewSetTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_list_videos(self):
        # Create some sample videos
        Video.objects.create(title='Video 1', description='Description 1')
        Video.objects.create(title='Video 2', description='Description 2')

        # Ensure the viewset lists videos when authenticated
        response = self.client.get('/content/videos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)  # Assuming 2 videos are created

    def test_create_video(self):
        # Ensure a video can be created when authenticated
        data = {'title': 'New Video', 'description': 'New Description'}
        response = self.client.post('/content/videos/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Video.objects.count(), 1)

    # Add more test cases for other functionalities (update, delete, etc.) as needed
