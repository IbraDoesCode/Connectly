from django.urls import reverse
import pytest
from django.contrib.auth.models import User
from rest_framework import status
from apps.users.factories import UserFactory
from apps.users.models import Profile



# Test Cases
@pytest.mark.django_db
def test_user_registration(api_client, mock_user_data, register_url):

    response = api_client.post(register_url, mock_user_data, secure=True, format='json')

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
    assert 'username' in response.data  # Ensure username validation error is present
    assert 'first_name' in response.data  # Ensure first_name is required
    assert 'last_name' in response.data  # Ensure last_name is required
    assert User.objects.filter(email="testuser@example.com").count() == 0  # Ensure no user is created


@pytest.mark.django_db
def test_create_admin_user(api_client, initialize_groups, mock_user_data):
    profile = UserFactory.create_admin_user(**mock_user_data)

    assert profile is not None
    assert profile.user.groups.filter(name='Admin').exists()


@pytest.mark.django_db
def test_get_users(admin_auth_client, get_all_users_url, mock_user_data):
    user1 = UserFactory.create_user_and_profile(**mock_user_data)

    response = admin_auth_client.get(get_all_users_url, secure=True)
    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert len(response_data) == 2 | 3 #included "or 3" incase a default user admin was initialized
    assert any(user['username'] == 'admin' for user in response_data)
    assert any(user['username'] == user1.user.username for user in response_data)


@pytest.mark.django_db
def test_get_users_logged_out(api_client, get_all_users_url, mock_user_data):

    response = api_client.get(get_all_users_url, secure=True)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_users_unauthorized(api_client, register_url, get_all_users_url, mock_user_data):
    register = api_client.post(register_url, mock_user_data, secure=True, format='json')

    token = register.data['access']
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    response = api_client.get(get_all_users_url, secure=True)
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_login_user(api_client, initialize_groups, token_login_url, get_all_users_url, mock_admin_data):
    admin = UserFactory.create_admin_user(**mock_admin_data)

    login = api_client.post(
        token_login_url,
        {
            'username': admin.user.username,
            'password': mock_admin_data['password'],
        },
        secure=True, format='json'
    )
    token = login.data['access']

    assert login.status_code == status.HTTP_200_OK
    assert token is not None

@pytest.mark.django_db
def test_update_user_success(auth_login_client, populate_users, update_user_url):
    user1, _, _ = populate_users
    client = auth_login_client(user1.user.username, "1234")
    url = update_user_url(user1.user.id)
    data = {"username": "new_username"}
    
    response = client.patch(url, data, format='json')
    
    assert response.status_code == status.HTTP_200_OK
    user1.user.refresh_from_db()
    assert user1.user.username == "new_username"

@pytest.mark.django_db
def test_update_user_no_changes(auth_login_client, populate_users, update_user_url):
    user1, _, _ = populate_users
    client = auth_login_client(user1.user.username, "1234")
    url = update_user_url(user1.user.id)
    data = {"username": user1.user.username}
    
    response = client.patch(url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Provided values are the same as the current user data."

@pytest.mark.django_db
def test_update_user_empty_body(auth_login_client, populate_users, update_user_url):
    user1, _, _ = populate_users
    client = auth_login_client(user1.user.username, "1234")
    url = update_user_url(user1.user.id)
    data = {}
    
    response = client.patch(url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Request body is empty. Provide at least one field to update."

@pytest.mark.django_db
def test_update_user_duplicate_username(auth_login_client, populate_users, update_user_url):
    user1, user2, _ = populate_users
    client = auth_login_client(user1.user.username, "1234")
    url = update_user_url(user1.user.id)
    data = {"username": user2.user.username}
    
    response = client.patch(url, data, format='json')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["username"] == ["A user with that username already exists."]

@pytest.mark.django_db
def test_update_user_not_found(auth_login_client, populate_users, update_user_url):
    user1, _, _ = populate_users
    client = auth_login_client(user1.user.username, "1234")
    url = update_user_url(9999)  # Non-existing user ID
    data = {"username": "new_username"}
    
    response = client.patch(url, data, format='json')
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "User not found."

@pytest.mark.django_db
def test_delete_user_success(auth_login_client, populate_users, update_user_url):
    user1, _, _ = populate_users
    client = auth_login_client(user1.user.username, "1234")
    url = update_user_url(user1.user.id)
    
    response = client.delete(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["detail"] == f"User deleted successfully."
    assert not User.objects.filter(id=user1.user.id).exists()

@pytest.mark.django_db
def test_delete_user_not_found(auth_login_client, populate_users, update_user_url):
    user1, _, _ = populate_users
    client = auth_login_client(user1.user.username, "1234")
    url = update_user_url(9999)  # Non-existing user ID
    
    response = client.delete(url)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["detail"] == "User not found."


@pytest.mark.django_db
def test_change_user_role(api_client, admin_auth_client, get_all_users_url, change_role_url, mock_user_data, register_url):
    admin_creds = admin_auth_client._credentials
    # Register new user
    register = api_client.post(register_url, mock_user_data, secure=True, format='json')
    user = User.objects.get(username=mock_user_data['username'])
    token = register.data['access']
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    user_creds = api_client._credentials

    # Try to access Get Users endpoint
    response1 = api_client.get(get_all_users_url, secure=True)
    assert response1.status_code == status.HTTP_403_FORBIDDEN

    # Add to admin role
    admin_auth_client.credentials(**admin_creds)
    role_response = admin_auth_client.post(change_role_url(user.id), { "role": "Admin" }, secure=True, format='json')
    assert role_response.status_code == status.HTTP_200_OK

    # Access Get Users again
    api_client.credentials(**user_creds)
    response2 = api_client.get(get_all_users_url, secure=True)
    assert response2.status_code == status.HTTP_200_OK

    # Change to moderator role
    admin_auth_client.credentials(**admin_creds)
    role_response = admin_auth_client.post(change_role_url(user.id), { "role": "Moderator" }, secure=True, format='json')
    assert role_response.status_code == status.HTTP_200_OK

    # Access Get Users again
    api_client.credentials(**user_creds)
    response2 = api_client.get(get_all_users_url, secure=True)
    assert response1.status_code == status.HTTP_403_FORBIDDEN
    
@pytest.mark.django_db
def test_profile_search_suggestions_username(auth_client, populate_users):
    user1, _, _ = populate_users
    search_url = reverse('profile-search-suggestions') + "?search_query=user1"
    response = auth_client.get(search_url, secure=True)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1  # Expecting only user1
    assert response.data[0]['username'] == 'user1'
    assert response.data[0]['full_name'] == 'User1 Lastname1'

@pytest.mark.django_db
def test_profile_search_suggestions_fullname(auth_client, populate_users):
    _, user2, _ = populate_users
    search_url = reverse('profile-search-suggestions') + "?search_query=User2%20Lastname2"
    response = auth_client.get(search_url, secure=True)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1  # Expecting only user2
    assert response.data[0]['username'] == 'user2'
    assert response.data[0]['full_name'] == 'User2 Lastname2'

@pytest.mark.django_db
def test_profile_search_suggestions_incomplete_name(auth_client, populate_users):
    user1, _, _ = populate_users
    search_url = reverse('profile-search-suggestions') + "?search_query=user"
    response = auth_client.get(search_url, secure=True)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1  # Expecting multiple users
    assert response.data[0]['username'] == 'test_user'
    assert response.data[0]['full_name'] == 'Test User'

@pytest.mark.django_db
def test_profile_search_suggestions_case_insensitive(auth_client, populate_users):
    _, user2, _ = populate_users
    search_url = reverse('profile-search-suggestions') + "?search_query=uSeR2%20LaStNaMe2"
    response = auth_client.get(search_url, secure=True)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1  # Expecting only user2
    assert response.data[0]['username'] == 'user2'
    assert response.data[0]['full_name'] == 'User2 Lastname2'

@pytest.mark.django_db
def test_profile_search_suggestions_no_query(auth_client):
    search_url = reverse('profile-search-suggestions')
    response = auth_client.get(search_url, secure=True)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'detail' in response.data
    assert response.data['detail'] == 'Search query is required.'

@pytest.mark.django_db
def test_profile_search_suggestions_no_match(auth_client):
    search_url = reverse('profile-search-suggestions') + "?search_query=NonExistent"
    response = auth_client.get(search_url, secure=True)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0  # No results found

@pytest.mark.django_db
def test_get_own_profile(auth_client, populate_users):
    user1, _, _ = populate_users  # Use the first user
    auth_client.force_authenticate(user=user1.user)
    profile_url = reverse('user-profile')
    response = auth_client.get(profile_url, secure=True)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == user1.first_name
    assert response.data['last_name'] == user1.last_name

@pytest.mark.django_db
def test_get_own_profile_not_authenticated(api_client):
    profile_url = reverse('user-profile')
    response = api_client.get(profile_url, secure=True)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_get_profile_by_id(auth_client, populate_users):
    user1, user2, _ = populate_users
    profile_url = reverse('user-profile-from-id', kwargs={'user_id': user2.user.id})
    response = auth_client.get(profile_url, secure=True)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == user2.first_name
    assert response.data['last_name'] == user2.last_name

@pytest.mark.django_db
def test_get_profile_by_invalid_id(auth_client):
    profile_url = reverse('user-profile-from-id', kwargs={'user_id': 9999})
    response = auth_client.get(profile_url, secure=True)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert 'detail' in response.data
    assert response.data['detail'] == 'Profile not found.'
    
import pytest
from rest_framework import status

@pytest.mark.django_db
def test_get_personal_comments_success(auth_login_client, personal_comments_url, populate_comments):
    comm1, _, _, _ = populate_comments
    client = auth_login_client(comm1.author.username, '1234')
    response = client.get(personal_comments_url(), secure=True, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)
    assert len(response.data) > 0  # Ensure user has comments


@pytest.mark.django_db
def test_get_personal_comments_empty(auth_client, personal_comments_url):
    response = auth_client.get(personal_comments_url(), secure=True, format='json')  
    assert response.status_code == status.HTTP_404_NOT_FOUND 
    assert response.data["Message"] == "No comments found"


@pytest.mark.django_db
def test_unauthenticated_user_access(api_client, personal_comments_url):
    response = api_client.get(personal_comments_url(), secure=True, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
