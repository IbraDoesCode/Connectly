from tokenize import TokenError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User, Group

from utils.logger import Logger
from utils.response_factory import ResponseFactory
from .factories import UserFactory
from .models import Profile
from .permissions import IsAdmin
from .serializers import UserSerializer, RoleSerializer

logger = Logger().get_logger()

class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = Profile.objects.all()
        serializer = UserSerializer(users, many=True)
        return ResponseFactory.success(
            serializer.data,
            serializer.data,
        )


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return ResponseFactory.bad_request(
                f"An error occurred when adding the user: {serializer.errors}",
                serializer.errors
            )

        try:
            user = serializer.save().user

            # Generate refresh & access tokens
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return ResponseFactory.created(
                f"User {user} created successfully",
                {
                    'access': str(access),
                    'refresh': str(refresh)
                }
            )

        except TokenError as e:
            return ResponseFactory.bad_request(
                f"Error while generating tokens: {str(e)}",
                {"detail": "Token generation failed."}
            )



class UserRoleView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, user_id):
        serializer = RoleSerializer(data=request.data)

        if not serializer.is_valid():
            return ResponseFactory.bad_request(
                "Error adding role to the user",
                serializer.errors
            )
        role = serializer.validated_data['role']

        try:
            user = User.objects.get(id=user_id)
            UserFactory.assign_user_role(user, role)

            return ResponseFactory.success(
                f"User {user.username} has been added to the {role} group",
            )

        except User.DoesNotExist:
            return ResponseFactory.not_found(
                "User not found",
                {"detail": "User not found."}
            )
