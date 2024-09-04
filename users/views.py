from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from users.models import CustomUser
from users.serializers import UserItemSerializer, SetNewPasswordSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate

# Create your views here.
class ListUsers(APIView):
    """ View to load all users from the database. """
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        users = CustomUser.objects.all() 
        serializer = UserItemSerializer(users, many=True)
        return Response(serializer.data)

class CurrentUserView(APIView):
    """ View to load the current logged in user from the database. """
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id
        })

class LoginView(ObtainAuthToken):
    """ View to login a user """

    def post(self, request, *args, **kwargs):
        # Get the username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            # Try to get the user from the database
            user = CustomUser.objects.get(username=username)
            
            # Check if the user is inactive
            if not user.is_active:
                return Response({"error": "This account is inactive. Please activate your account."},
                                status=status.HTTP_403_FORBIDDEN)

            # Authenticate the user if active
            user = authenticate(username=username, password=password)
            if user is not None:
                # Generate token if the user is authenticated and active
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'email': user.email
                })
            else:
                return Response({"error": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)
        
        except CustomUser.DoesNotExist:
            return Response({"error": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    """ View to register a user including error responses. """

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create the user with is_active=False
            user = CustomUser.objects.create_user(
                username=username, email=email, password=password, first_name=first_name, last_name=last_name, is_active=False)
            
            # Generate activation token and send activation email
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = f"{request.scheme}://{request.get_host()}/api/v1/activate/{uidb64}/{token}/"

            # Send activation email
            send_mail(
                subject="Activate your account",
                message=f"Click the link to activate your account: {activation_link}",
                from_email="noreply@yourapp.com",
                recipient_list=[email],
            )

            return Response({"message": "User created successfully. Check your email for activation link."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ActivateAccountView(APIView):
    """ View to activate the user account when the user clicks the activation link """

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({"error": "Invalid activation link."}, status=status.HTTP_400_BAD_REQUEST)

        # Check token
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Activation link is invalid or has expired."}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        # Continue the process for password reset token generation...
        return Response({"detail": "Password reset link sent."}, status=status.HTTP_200_OK)
    
class SetNewPasswordView(APIView):
    """
    View to handle setting a new password without requiring the old password.
    This is used when a user forgets their password and resets it via a token.
    """
    def post(self, request, uidb64, token):
        try:
            # Decode the user id
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            return Response({"error": "Invalid token or user does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the token is valid
        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate the new password and confirm password
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)