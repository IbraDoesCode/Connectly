import requests
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class GoogleAuthentication(BaseAuthentication):
    """
    Custom authentication backend to validate Google OAuth2 access tokens.
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # Don't authenticate if no token is provided

        access_token = auth_header.split(" ")[1]

        try:
            # Validate token with Google's Userinfo API
            response = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )

            if response.status_code != 200:
                raise AuthenticationFailed("Invalid Google token.")

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
