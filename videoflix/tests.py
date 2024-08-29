from django.test import TestCase, Client
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from users.models import CustomUser
from videoflix.models import Video
from videoflix.serializers import VideoItemSerializer
from rest_framework import status

# Create your tests here.
    # Test loading all videos.
class VideosAPITest(TestCase):
    # Tests for videos listing and creation

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='test_user', password='test_password', email='test@example.com')
        self.token = Token.objects.create(user=self.user)
        
    def test_list_videos(self):
        self.client.force_authenticate(user=self.user, token=self.token)

        # Send GET request to list videos
        response = self.client.get('/api/v1/videos/')

        # Assert response status and content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming no videos exist initially
        self.assertEqual(len(response.data), 0)