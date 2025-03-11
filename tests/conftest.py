import io
import json
from django.test import override_settings
from django.conf import settings
import pytest
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from rest_framework.test import APIClient

from apps.posts.factories import PostFactory, CommentFactory
from apps.users.factories import UserFactory
from django.contrib.auth.models import Group

from utils.config_manager import ConfigManager
from utils.rate_limiter import RateLimiterFactory

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

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
def update_user_url():
    def _generate_url(user_id):
        return reverse('user-update', kwargs={'user_id': user_id})
    return _generate_url

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
def personal_posts_url():
    def _generate_url():
        return reverse('personal-posts')
    return _generate_url

@pytest.fixture
def personal_comments_url():
    def _generate_url():
        return reverse('personal-comments')
    return _generate_url

@pytest.fixture
def follow_url():
    def _generate_url(user_id, query_kwargs=None):
        url = reverse('profiles:user-follow', kwargs={'user_id': user_id})
        if query_kwargs:
            print(f'{url}?{urlencode(query_kwargs)}')
            return f'{url}?{urlencode(query_kwargs)}'
        return url
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

# Media File Fixtures
@pytest.fixture
def test_image():
    # Create a test image in memory
    file = io.BytesIO()
    image = Image.new('RGB', (100, 100), color='red')
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return SimpleUploadedFile('test.png', file.read(), content_type='image/png')

@pytest.fixture
def test_video():
    """Create a minimal valid MP4 file"""
    # This is a minimal valid MP4 file header
    mp4_header = (
        b'\x00\x00\x00\x20\x66\x74\x79\x70\x69\x73\x6F\x6D\x00\x00\x02\x00'
        b'\x69\x73\x6F\x6D\x69\x73\x6F\x32\x6D\x70\x34\x31\x00\x00\x00\x08'
        b'\x6D\x6F\x6F\x76'
    )
    return SimpleUploadedFile(
        'test.mp4',
        mp4_header,
        content_type='video/mp4'
    )

@pytest.fixture
def test_invalid_image():
    # Create a small test image with invalid format
    image_content = b'fake image content'
    return SimpleUploadedFile('test.txt', image_content, content_type='image/png')

@pytest.fixture
def test_invalid_video():
    # Create a small test video with invalid format
    video_content = b'fake video content'
    return SimpleUploadedFile('test.txt', video_content, content_type='video/mp4')

@pytest.fixture
def mock_post_with_image_data(test_image):
    return {
        "content": "Test Post with Image",
        "post_type": "image",
        "media_files": [test_image]
    }

@pytest.fixture
def mock_post_with_video_data(test_video):
    return {
        "content": "Test Post with Video",
        "post_type": "video",
        "videos": [test_video]
    }
    
@pytest.fixture
def mock_post_with_invalid_image(test_invalid_image):
    return {
        "content": "Test Post with Image",
        "post_type": "image",
        "images": [test_invalid_image]
    }

@pytest.fixture
def mock_post_with_invalid_video(test_invalid_video):
    return {
        "content": "Test Post with Video",
        "post_type": "video",
        "videos": [test_invalid_video]
    }
    
@pytest.fixture
def mock_comment_with_image_data(test_image):
    return {
        "content": "Test Comment with Image",
        "comment_type": "image",
        "image": test_image
    }
    
@pytest.fixture
def mock_comment_with_invalid_image(test_invalid_image):
    return {
        "content": "Test Comment with Image",
        "comment_type": "image",
        "image": test_image
    }
    
@pytest.fixture()
def mock_image_processing(monkeypatch):
    """Mock image processing to avoid actual operations with PIL"""

    def mock_compress_image(image, output_path=None, quality=85, max_width=1200, max_height=1200):
        return image

    def mock_extract_image_metadata(image_file):
        return {
            'width': 800,
            'height': 600,
            'file_size': len(image_file.read()),
            'file_type': 'JPEG'
        }

    from utils.media_compressor import MediaCompressor
    monkeypatch.setattr(MediaCompressor, 'compress_image', mock_compress_image)
    monkeypatch.setattr(MediaCompressor, 'extract_image_metadata', mock_extract_image_metadata)

@pytest.fixture()
def mock_video_processing(monkeypatch):
    """Mock video processing to avoid actual ffmpeg operations"""
    def mock_compress_video(video_file):
        return video_file
        
    def mock_extract_metadata(video_file):
        return {
            'width': 1280,
            'height': 720,
            'duration': 10.0,
            'file_size': len(video_file.read())
        }
    
    from utils.media_compressor import MediaCompressor
    monkeypatch.setattr(MediaCompressor, 'compress_video', mock_compress_video)
    monkeypatch.setattr(MediaCompressor, 'extract_video_metadata', mock_extract_metadata)

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