from django.urls import path
from .views import UserListView, UserRegistrationView, UserRoleView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('role/<int:user_id>', UserRoleView.as_view(), name='user-role-change'),
]