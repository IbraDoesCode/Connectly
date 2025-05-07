from django.urls import path
from .views import *

urlpatterns = [
    # Admin Routes
    path('', UserListView.as_view(), name='user_list'),
    path('<int:user_id>', UserUpdateView.as_view(), name='user-update'),
    path('signup/', UserSignupView.as_view(), name='user-register'),
    path('role/<int:user_id>', UserRoleView.as_view(), name='user-role-change'),
]

profile_patterns = [
    # Profile Routes
    path('feed/', FeedView.as_view(), name='user-feed'),
    path('', ProfileQueryView.as_view(), name='user-profiles'),
    path('suggestions/', SuggestedUsersView.as_view(), name='follow-suggestions'),
    path('<str:user_id>/', ProfileDetailView.as_view(), name='user-profile-from-id'),
    path('<str:user_id>/posts/', ProfilePostsView.as_view(), name='user-posts'),
    path('<str:user_id>/comments/', ProfileCommentsView.as_view(), name='user-comments'),
    path('<str:user_id>/follow/', FollowView.as_view(), name='user-follow'),
]