import requests
import jwt
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication  # If using Simple JWT

class GoogleAuthentication(BaseAuthentication):
    """
    Custom authentication backend to validate Google OAuth2 access tokens.
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # Don't authenticate if no token is provided

        access_token = auth_header.split(" ")[1]

        # Check if the token is a JWT issued by Django
        if self.is_django_jwt(access_token):
            return None  # Let Django's own JWT middleware handle it

        try:
            # Validate token with Google's Userinfo API
            response = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )

            if response.status_code != 200:
                raise AuthenticationFailed("Invalid token.")

            user_data = response.json()
            email = user_data.get("email")
            first_name = user_data.get("given_name", "")
            last_name = user_data.get("family_name", "")

            if not email:
                raise AuthenticationFailed("Invalid Google token. No email found.")

            # Get or create the user
            user, created = User.objects.get_or_create(email=email, defaults={"username": email, "first_name": first_name, "last_name": last_name})

            return (user, None)

        except Exception as e:
            raise AuthenticationFailed(f"Authentication error: {str(e)}")

    def is_django_jwt(self, token):
        """
        Checks if the token is a valid JWT issued by Django (Simple JWT).
        """
        try:
            # Decode token without verification
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            
            # Check if it has Django's expected claims (e.g., user_id)
            if "user_id" in decoded_token:
                # Optionally verify with Django's Simple JWT
                jwt_authenticator = JWTAuthentication()
                validated_token = jwt_authenticator.get_validated_token(token)
                
                if validated_token:
                    return True
        except Exception:
            pass

        return False
