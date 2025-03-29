from tokenize import TokenError

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db.models import Q, Value
from django.db.models.functions import Concat
from apps.posts.models import Comment, Post
from apps.posts.permissions import IsAuthor
from apps.posts.serializers import CommentSerializer, PostSerializer, PostFeedSerializer
from utils.logger import Logger
from utils.response_factory import ResponseFactory
from .factories import UserFactory
from .models import Profile, Follow
from .permissions import IsAdmin, IsOwnerOrAdmin
from .serializers import ProfileSearchSerializer, ProfileSerializer, UserSerializer, RoleSerializer, \
    UserUpdateSerializer, FollowListSerializer
from rest_framework.generics import ListAPIView
from .serializers import ProfileSearchSerializer, UserSerializer, RoleSerializer, FollowSerializer # UnfollowSerializer


# ==============================================================================
# User Endpoints
# ==============================================================================

class UserListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        users = self.paginate_queryset(Profile.objects.all()) # Apply pagination

        # Serialize the paginated queryset
        serializer = UserSerializer(users, many=True)

        # Return the paginated response (with pagination metadata like 'next', 'previous')
        return ResponseFactory.success(serializer.data, self.get_paginated_response(serializer.data).data)

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            
            # Check if request body is empty
            if not request.data:
                return ResponseFactory.bad_request(
                    "No changes were provided.",
                    {"detail": "Request body is empty. Provide at least one field to update."}
                )
            
            
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)

            if not serializer.is_valid():
                return ResponseFactory.bad_request(
                    f"Error updating user {user.username}",
                    serializer.errors
                )
                
                
            # Check if provided data is identical to current user data
            if all(getattr(user, field) == value for field, value in request.data.items()):
                return ResponseFactory.bad_request(
                    "No changes detected.",
                    {"detail": "Provided values are the same as the current user data."}
                )

            updated_user = serializer.save()

            return ResponseFactory.success(
                f"User {updated_user.username} updated successfully",
                serializer.data
            )

        except User.DoesNotExist:
            return ResponseFactory.not_found(
                "User not found",
                {"detail": "User not found."}
            )
        except Exception as e:
            return ResponseFactory.bad_request(
                f"An error occurred when updating the user: {str(e)}",
                {"detail": "An error occurred when updating the user."}
            )


    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)

            user.delete()

            return ResponseFactory.success(
                f"User {user.username} deleted successfully",
                {"detail": "User deleted successfully."}
            )

        except User.DoesNotExist as e:
            return ResponseFactory.not_found(
                "User not found.",
                {"detail": "User not found."}
            )
        except Exception as e:
            return ResponseFactory.bad_request(
                f"An error occurred when deleting the user: {str(e)}",
                {"detail": "An error occurred when deleting the user."}
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
                {"detail": "Role has been updated."}
            )

        except User.DoesNotExist:
            return ResponseFactory.not_found(
                "User not found",
                {"detail": "User not found."}
            )

# ==============================================================================
# Profile Endpoints
# ==============================================================================

class FeedView(generics.ListAPIView):
    serializer_class = PostFeedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        followed_users = Follow.objects.filter(follower=user).values_list('followed', flat=True)
        feed_type = self.request.query_params.get('feed_type', 'public')

        # Default feed type
        posts = Post.objects.filter(privacy_type='public').order_by('-created_at')

        if feed_type == 'following':
            posts = Post.objects.filter(
                Q(author__id__in=followed_users, privacy_type='followers') |
                Q(author__id__in=followed_users, privacy_type='public') |
                Q(author=user)
            ).order_by('-created_at').distinct()
        
        return posts

class ProfileQueryView(APIView):
    """
    Returns a list of profiles based on a search query.

    The search query can be a username, first name, last name, or a combination
    of the three.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.GET.get('search_query', '')

        if not search_query:
            return ResponseFactory.bad_request(
                "Search query is required",
                {"detail": "Search query is required."}
            )

        try:
            # Combine first and last name as a searchable field
            profiles = Profile.objects.annotate(
                full_name=Concat('first_name', Value(' '), 'last_name')
            ).filter(
                Q(user__username__icontains=search_query) |
                Q(full_name__icontains=search_query)  # Enables full name search!
            ).only('id', 'user__username', 'first_name', 'last_name')

            serializer = ProfileSearchSerializer(profiles, many=True)

            return ResponseFactory.success(
                serializer.data,
                serializer.data
            )
        except Exception as e:
            return ResponseFactory.bad_request(
                f"An error occurred while processing the request: {str(e)}",
                {"detail": "An error occurred while processing the request."}
            )

class ProfileDetailView(APIView):
    """
    Returns the profile of the authenticated user.
    """

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAuthor()]

    def get(self, request, user_id):
        try:
            if user_id == "me":
                user = Profile.objects.get(user=request.user)
            else:
                user = Profile.objects.get(user__id=user_id)

            serializer = UserSerializer(user)
            return ResponseFactory.success(
                serializer.data,
                serializer.data
            )

        except Profile.DoesNotExist:
            return ResponseFactory.not_found(
                "Profile not found",
                {"detail": "Profile not found."}
            )
        except Exception as e:
            return ResponseFactory.bad_request(
                f"An error occurred while processing the request: {str(e)}",
                {"detail": "An error occurred while processing the request."}
            )

    def patch(self, request, user_id=None):
        try:
            user = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(user, data=request.data, partial=True)
            
            # Check if request body is empty
            if not request.data:
                return ResponseFactory.bad_request(
                    "No changes were provided.",
                    {"detail": "Request body is empty. Provide at least one field to update."}
                )

            if not serializer.is_valid():
                return ResponseFactory.bad_request(
                    "Error while updating the profile",
                    serializer.errors
                )
                
            # Check if provided data is identical to current user data
            if all(getattr(user, field) == value for field, value in request.data.items()):
                return ResponseFactory.bad_request(
                    "No changes detected.",
                    {"detail": "Provided values are the same as the current user data."}
                )

            serializer.save()
            return ResponseFactory.success(
                "Profile updated successfully",
                serializer.data
            )
        except Profile.DoesNotExist:
            return ResponseFactory.not_found(
                "Profile not found",
                {"detail": "User not found."}
            )

    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return ResponseFactory.success(
                "Profile deleted successfully",
                {'Message': 'Profile deleted successfully'}
            )
        except User.DoesNotExist:
            return ResponseFactory.not_found(
                "Profile not found",
                {'Message': 'Profile not found.'}
            )


class ProfileCommentsView(APIView):
    permission_classes = [IsAuthenticated, IsAuthor]

    def get(self, request):
        comments = Comment.objects.filter(author=request.user)

        if not comments.exists():
            return ResponseFactory.not_found(
                "No comments found",
                {'Message': 'No comments found'}
            )

        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return ResponseFactory.success(
            serializer.data,
            serializer.data
        )
    
class ProfilePostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            if user_id == "me":
                user = request.user
            else:
                user = User.objects.get(id=user_id)

            posts = Post.objects.filter(author=user)

            serializer = PostSerializer(posts, many=True, context={'request': request})
            return ResponseFactory.success(
                serializer.data,
                serializer.data
            )
        except Profile.DoesNotExist:
            return ResponseFactory.not_found(
                "Profile not found",
                {"detail": "Profile not found."}
            )
        except Exception as e:
            return ResponseFactory.bad_request(
                f"An error occurred while processing the request: {str(e)}",
                {"detail": f"An error occurred while processing the request."}
            )

class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            query_type = request.query_params.get('type', None)

            if query_type not in ['following', 'follower']:
                return ResponseFactory.bad_request(
                    "Invalid type",
                    {"detail": "Invalid type. Use 'following' or 'follower'."}
                )

            user = User.objects.get(id=user_id)

            if query_type == 'follower':
                queryset = Follow.objects.filter(followed=user)
            else:
                queryset = Follow.objects.filter(follower=user)

            serializer = FollowListSerializer(queryset, many=True, context={"request": request})

            return ResponseFactory.success(
                serializer.data,
                serializer.data
            )

        except User.DoesNotExist:
            return ResponseFactory.not_found(
                "No user found",
                {'Message': 'No user found'}
            )
        except Exception as e:
            return ResponseFactory.bad_request(
                "Error retrieving followers",
                {"detail": str(e)}
            )


    def post(self, request, user_id):
        try:
            serializer = FollowSerializer(data={"user_id": user_id}, context={'request': request})

            if serializer.is_valid():
                result = serializer.save()

                if isinstance(result, dict):
                    return ResponseFactory.success('Unfollowed Successfully', {'Message': 'Unfollowed successfully'})

                return ResponseFactory.created("Followed Successfully", {"Message": "Followed successfully"})

            return ResponseFactory.bad_request("Error", {"Error": serializer.errors})

        except User.DoesNotExist:
            return ResponseFactory.not_found(
                "No user found",
                {'Message': 'No user found'}
            )
        except Exception as e:
            return ResponseFactory.bad_request(
                "Error following the user",
                {"detail": str(e)}
            )


