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

class GoogleVerifyTokenView(APIView):
    def post(self, request):
        token = request.data.get('access_token')

        if token is None:
            return ResponseFactory.bad_request('No token found', {'detail': 'Token is required'})
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), audience=os.getenv('GOOGLE_CLIENT_ID'))
            email = idinfo['email']

            user = User.objects.get(email=email)

            refresh = RefreshToken.for_user(user)
            return ResponseFactory.success('Social sign in success', {'refresh': str(refresh), 'access': str(refresh.access_token)})
        except User.DoesNotExist:
            return ResponseFactory.success('Social sign up success', {'signup_complete': False})
        except (ValueError, GoogleAuthError) as e:
            return ResponseFactory.bad_request('Google token verification failed', {'error': str(e)})        
        except Exception as e:
            return ResponseFactory.server_error('Unhandled exception during Google login', {'error': str(e)})
        
class CompleteSignupView(APIView):
    def post(self, request):
        token = request.data.get('access_token')
        username = request.data.get('username')

        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), audience=os.getenv('GOOGLE_CLIENT_ID'))

            first_name = idinfo.get('given_name')
            last_name = idinfo.get('family_name')
            email = idinfo['email']

            if User.objects.filter(username=username).exists():
                return ResponseFactory.bad_request('Username already taken', {'detail': 'This username is already in use.'})
            
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.set_unusable_password()
            user.save()

            UserFactory.create_profile_for_existing_user(user)

            refresh = RefreshToken.for_user(user)
            return ResponseFactory.success('Social sign in success', {'refresh': str(refresh), 'access': str(refresh.access_token)})

        except (ValueError, GoogleAuthError) as e:
            return ResponseFactory.bad_request('Google token verification failed', {'error': str(e)})        
        except Exception as e:
            return ResponseFactory.internal_server_error('Unhandled exception during Google login', {'error': str(e)})
