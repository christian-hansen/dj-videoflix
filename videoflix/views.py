from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.views.decorators.cache import cache_page
from videoflix.models import Video
from videoflix.serializers import VideoItemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# @cache_page(CACHE_TTL)
# # def

class ListVideos(APIView):
    """ View to load all videos from the database """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        tasks = Video.objects.all() 
        serializer = VideoItemSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data.copy()  # Make a copy of the request data

        serializer = VideoItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Save the data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
