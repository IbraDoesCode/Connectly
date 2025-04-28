import os
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from utils.response_factory import ResponseFactory
from django.contrib.auth.models import User
from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.exceptions import GoogleAuthError
from apps.users.factories import UserFactory

load_dotenv()

class LogoutView(APIView):
     def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            return Response({"detail": "Successfully logged out."}, status=200)
        except Exception as e:
            return Response({"error": "Invalid token or already logged out."}, status=400)

class GoogleLoginView(APIView):
    def post(self, request):
        # Retrieve google token from request
        token = request.data.get('access_token')

        # Verify google token and retrieve user info
        if token is None:
            return ResponseFactory.bad_request('No token found', {'detail': 'Token is required'})
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), audience=os.getenv('GOOGLE_CLIENT_ID'))

            email = idinfo['email']
            first_name = idinfo['given_name']
            last_name = idinfo['family_name']
            username = email.split('@')[0]

            # Create or find user
            user, created = User.objects.get_or_create(
                email=email, 
                defaults={'first_name': first_name, 'last_name': last_name, 'username': username}
            )

            # Only create for new users
            if created:
                UserFactory.create_profile_for_existing_user(user)

            refresh = RefreshToken.for_user(user)

            # Return jwt tokens
            return ResponseFactory.success('Social sign success', {'refresh': str(refresh), 'access': str(refresh.access_token)})
        except (ValueError, GoogleAuthError) as e:
            return ResponseFactory.bad_request('Google token verification failed', {'error': str(e)})        
        except Exception as e:
            return ResponseFactory.server_error('Unhandled exception during Google login', {'error': str(e)})