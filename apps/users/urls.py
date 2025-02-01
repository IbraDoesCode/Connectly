from django.urls import path
from .views import UserListView, UserRegistrationView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
]