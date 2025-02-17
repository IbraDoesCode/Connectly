import json
from django.test import override_settings
from django.conf import settings
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from apps.posts.factories import PostFactory, CommentFactory
from apps.users.factories import UserFactory
from django.contrib.auth.models import Group

from utils.config_manager import ConfigManager
from utils.rate_limiter import RateLimiterFactory

# Initializer Fixtures
@pytest.fixture
def initialize_groups():
    Group.objects.get_or_create(name='Admin')
    Group.objects.get_or_create(name='Moderator')
    
@pytest.fixture(autouse=True)
def disable_throttling(request):
    original_rest_framework = settings.REST_FRAMEWORK.copy()
    new_rest_framework = {
        **original_rest_framework,
        'DEFAULT_THROTTLE_CLASSES': [],
        'DEFAULT_THROTTLE_RATES': {},
    }
    
    with override_settings(REST_FRAMEWORK=new_rest_framework):
        yield

# Client Fixtures
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(api_client, initialize_groups, register_url, mock_user_data):
    response = api_client.post(register_url, mock_user_data, secure=True, format='json')
    
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    return api_client

@pytest.fixture
def auth_login_client(api_client, initialize_groups, token_login_url):
    def _generate_client(username, password):
        response = api_client.post(
            token_login_url,
            {
                'username': username,
                'password': password
            },
            secure=True, format='json'
        )
        token = response.data['access']
        api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        return api_client
    return _generate_client


@pytest.fixture
def admin_auth_client(api_client, initialize_groups, register_url, mock_admin_data):
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

@pytest.fixture
def post_list_url():
    return reverse('post_list')

@pytest.fixture
def post_detail_url():
    def _generate_url(post_id):
        return reverse('post_detail', kwargs={'post_id': post_id})
    return _generate_url

@pytest.fixture
def comment_list_url():
    def _generate_url(post_id):
        return reverse('comment_list', kwargs={'post_id': post_id})
    return _generate_url

@pytest.fixture
def comment_detail_url():
    def _generate_url(post_id, comment_id):
        return reverse('comment_detail', kwargs={'post_id': post_id, 'comment_id': comment_id})
    return _generate_url

@pytest.fixture
def like_post_url():
    def _generate_url(post_id):
        return reverse('like_post', kwargs={'post_id': post_id})
    return _generate_url

@pytest.fixture
def like_comment_url():
    def _generate_url(post_id, comment_id):
        return reverse('like_comment', kwargs={'post_id': post_id, 'comment_id': comment_id})
    return _generate_url

@pytest.fixture
def personal_comments_url():
    def _generate_url():
        return reverse('personal-comments')
    return _generate_url

# Mock Data Fixtures
@pytest.fixture
def mock_user_data():
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
        "username": "test_admin",
        "email": "testadmin@super.com",
        "password": "1234",
        "first_name": "Admin",
        "last_name": "User",
    }
    return data

@pytest.fixture
def mock_post_data():
    data = {
        "content": "Test Posting",
        "post_type": "text",
    }
    return data

@pytest.fixture
def mock_comment_data():
    data = {
        "content": "Test Comment",
        "comment_type": "text",
    }
    return data


# Populate Database
@pytest.fixture
def populate_users():
    user1 = UserFactory.create_user_and_profile("user1","user1@email.com","1234",
                                                "User1","Lastname1")
    user2 = UserFactory.create_user_and_profile("user2","user2@email.com","1234",
                                                "User2","Lastname2")
    user3 = UserFactory.create_user_and_profile("user3","user3@email.com","1234",
                                                "User3","Lastname3")
    return user1, user2, user3

@pytest.fixture
def populate_posts(populate_users):
    user1, user2, user3 = populate_users
    post1 = PostFactory.create_post(user1.user, "text", "Post 1 of User1")
    post2 = PostFactory.create_post(user2.user, "text", "Post 1 of User2")
    post3 = PostFactory.create_post(user2.user, "text", "Post 2 of User2")
    post4 = PostFactory.create_post(user3.user, "text", "Post 1 of User3")
    return post1, post2, post3, post4

@pytest.fixture
def populate_comments(populate_posts):
    post1, post2, post3, post4 = populate_posts
    comm1 = CommentFactory.create_comment(post4, post1.author, "text", "Comm 1 of User1 on Post4")
    comm2 = CommentFactory.create_comment(post3, post2.author, "text", "Comm 1 of User2 on Post3")
    comm3 = CommentFactory.create_comment(post2, post3.author, "text", "Comm 2 of User2 on Post2")
    comm4 = CommentFactory.create_comment(post1, post4.author, "text", "Comm 1 of User3 on Post1")
    return comm1, comm2, comm3, comm4