import pytest
from django.contrib.auth.models import User
from rest_framework import status
from apps.users.factories import UserFactory
from apps.users.models import Profile



# Test Cases
@pytest.mark.django_db
def test_user_registration(api_client, mock_data, register_url):

    response = api_client.post(register_url, mock_data, secure=True, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert 'access' in response.data
    assert 'refresh' in response.data

    assert User.objects.filter(username='test_user').exists()
    user = User.objects.get(username='test_user')
    assert Profile.objects.filter(user=user).exists()

    assert user.email == "testuser@example.com"
    assert user.check_password("1234")


@pytest.mark.django_db
def test_user_registration_missing_field(api_client, register_url):
    data = {
      "username": "",
      "email": "testuser@example.com",
      "password": "1234"
    }

    response = api_client.post(register_url, data, secure=True, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'username' in response.data
    assert User.objects.count() == 0

@pytest.mark.django_db
def test_create_admin_user(api_client, initialize_groups, mock_data):
    profile = UserFactory.create_admin_user(**mock_data)

    assert profile is not None
    assert profile.user.groups.filter(name='Admin').exists()

@pytest.mark.django_db
def test_get_users(auth_client, get_all_users_url, mock_data):
    user1 = UserFactory.create_user_and_profile(**mock_data)

    response = auth_client.get(get_all_users_url, secure=True)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    print(response_data)
    assert len(response_data) == 2
    assert any(user['username'] == 'admin' for user in response_data)
    assert any(user['username'] == user1.user.username for user in response_data)

@pytest.mark.django_db
def test_get_users_logged_out(api_client, get_all_users_url, mock_data):

    response = api_client.get(get_all_users_url, secure=True)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_get_users_unauthorized(api_client, register_url, get_all_users_url, mock_data):
    register = api_client.post(register_url, mock_data, secure=True, format='json')

    token = register.data['access']
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    response = api_client.get(get_all_users_url, secure=True)
    assert response.status_code == status.HTTP_403_FORBIDDEN
