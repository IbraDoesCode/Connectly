from django.urls import path
from .views import *

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('role/<int:user_id>', UserRoleView.as_view(), name='user-role-change'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
    path('profile/<int:user_id>', ProfileByIDView.as_view(), name='user-profile-from-id'),
    path('profile/search/', ProfileSearchSuggestionsView.as_view(), name='profile-search-suggestions'), # * Usage: /users/profile/search/?search_query=*name*
    path('profile/comments/', PersonalCommentsView.as_view(), name='personal-comments'),
]