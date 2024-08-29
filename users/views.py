from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import CustomUser
from users.serializers import UserItemSerializer

# Create your views here.
class ListUsers(APIView):
    """ View to load all users from the database. """
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        users = CustomUser.objects.all() 
        serializer = UserItemSerializer(users, many=True)
        return Response(serializer.data)
    