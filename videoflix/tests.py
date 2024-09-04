from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from users.models import CustomUser
from videoflix.models import Video
from videoflix.serializers import VideoItemSerializer
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import time

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
        

class VideoUploadTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.upload_url = reverse('video-list')

    def test_video_upload_and_conversion(self):
        # Create temporary video and thumbnail files for testing
        video_content = b'a fake video content'
        thumbnail_content = b'a fake thumbnail content'
        video = SimpleUploadedFile("test_video.mp4", video_content, content_type="video/mp4")
        thumbnail = SimpleUploadedFile("thumbnail.jpg", thumbnail_content, content_type="image/jpg")

        # Upload the video and thumbnail
        response = self.client.post(self.upload_url, {
            'title': 'Test Video',
            'description': 'Test Description',
            'video_file': video,
            'thumbnail_file': thumbnail
        }, format='multipart')
        self.assertEqual(response.status_code, 201)

        # Check if the video object was created
        video_obj = Video.objects.get(title='Test Video')
        self.assertIsNotNone(video_obj)

        # Check if the file paths for 360p, 720p, and 1080p versions are correct
        video_path = video_obj.video_file.path
        thumbnail_path = video_obj.thumbnail_file.path
        base, ext = os.path.splitext(video_path)

        video_360p_path = f"{base}_360p{ext}"
        video_720p_path = f"{base}_720p{ext}"
        video_1080p_path = f"{base}_1080p{ext}"

        # Simulate conversion delay (if necessary)
        time.sleep(1)

        # TODO: Check if the converted video files exist
        # self.assertTrue(os.path.exists(video_360p_path))
        # self.assertTrue(os.path.exists(video_720p_path))
        # self.assertTrue(os.path.exists(video_1080p_path))

        # Clean up created files
        try:
            os.remove(video_path)
            os.remove(thumbnail_path)
            # os.remove(video_360p_path)
            # os.remove(video_720p_path)
            # os.remove(video_1080p_path)
        except FileNotFoundError:
            pass