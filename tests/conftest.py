import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from apps.users.factories import UserFactory
from django.contrib.auth.models import Group

# Initializer Fixtures
@pytest.fixture
def initialize_groups():
    Group.objects.get_or_create(name='Admin')
    Group.objects.get_or_create(name='Moderator')


# Client Fixtures
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(api_client, initialize_groups, register_url, mock_admin_data):
    response = api_client.post(register_url, mock_admin_data, secure=True, format='json')

    admin = User.objects.filter(username=mock_admin_data['username']).first()
    UserFactory.assign_user_role(admin, 'Admin')

    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    return api_client


# URL Fixtures
@pytest.fixture
def register_url():
    return reverse('user-register')

@pytest.fixture
def get_all_users_url():
    return reverse('user_list')

@pytest.fixture
def token_login_url():
    return reverse('token_obtain_pair')

@pytest.fixture
def change_role_url():
    def _generate_url(user_id):
        return reverse('user-role-change', kwargs={'user_id': user_id})
    return _generate_url

# Mock Data Fixtures
@pytest.fixture
def mock_data():
    data = {
        "username": "test_user",
        "email": "testuser@example.com",
        "password": "1234",
        "first_name": "Test",
        "last_name": "User",
    }
    return data

@pytest.fixture
def mock_admin_data():
    data = {
        "username": "admin",
        "email": "admin@super.com",
        "password": "1234",
        "first_name": "Admin",
        "last_name": "User",
    }
    return data