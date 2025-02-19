from django.urls import path
from .views import *

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('<int:user_id>', UserUpdateView.as_view(), name='user-update'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('role/<int:user_id>', UserRoleView.as_view(), name='user-role-change'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
    path('profile/<int:user_id>', ProfileByIDView.as_view(), name='user-profile-from-id'),
    path('profile/search/', ProfileSearchSuggestionsView.as_view(), name='profile-search-suggestions'), # * Usage: /users/profile/search/?search_query=*name*
    path('profile/posts/', PersonalPostsView.as_view(), name='personal-posts'),
    path('profile/comments/', PersonalCommentsView.as_view(), name='personal-comments'),
    path('follow/', FollowView.as_view(), name='follow'),
    path('unfollow/', UnfollowView.as_view(), name='unfollow'),
]