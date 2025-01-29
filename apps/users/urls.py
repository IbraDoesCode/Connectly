from django.urls import path
from .views import UserListView, UserRegistrationView, UserLoginView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login')
]