import pytest
import io
from rest_framework import status
from django.contrib.auth.models import User
from apps.posts.models import Post, Media
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

# Test Cases
@pytest.mark.django_db
def test_create_post(auth_client, post_list_url, mock_post_data):

    response = auth_client.post(post_list_url, mock_post_data, secure=True, format='json')

    post = response.data
    assert response.status_code == status.HTTP_201_CREATED
    assert post['content'] == mock_post_data['content']
    assert Post.objects.count() == 1

    auth_client.post(post_list_url, mock_post_data, secure=True, format='json')
    assert Post.objects.count() == 2

@pytest.mark.django_db
def test_create_post_with_image(auth_client, post_list_url, mock_post_with_image_data, mock_image_processing):
    response = auth_client.post(post_list_url, mock_post_with_image_data, secure=True, format='multipart')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert Post.objects.count() == 1
    assert Media.objects.count() == 1
    assert 'post_images' in response.data
    assert len(response.data['post_images']) == 1

@pytest.mark.django_db
def test_create_post_with_invalid_image(auth_client, post_list_url, mock_post_with_invalid_image):
    response = auth_client.post(post_list_url, mock_post_with_invalid_image, secure=True, format='multipart')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_create_image_post_missing_image(auth_client, post_list_url):
    data = {
        "content": "Test Post",
        "post_type": "image"
    }
    response = auth_client.post(post_list_url, data, secure=True, format='multipart')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Image posts must include at least one image" in str(response.data)

# Post Video Tests
@pytest.mark.django_db
def test_create_post_with_video(auth_client, post_list_url, mock_post_with_video_data, mock_video_processing):
    data = mock_post_with_video_data.copy()

    response = auth_client.post(post_list_url, data, secure=True, format='multipart')
    
    if response.status_code != status.HTTP_201_CREATED:
        print("Response data:", response.data)  # Debug info
        
    assert response.status_code == status.HTTP_201_CREATED
    assert Post.objects.count() == 1
    assert Media.objects.count() == 1
    assert 'post_videos' in response.data
    assert len(response.data['post_videos']) == 1

@pytest.mark.django_db
def test_create_post_with_invalid_video(auth_client, post_list_url, mock_post_with_invalid_video):
    response = auth_client.post(post_list_url, mock_post_with_invalid_video, secure=True, format='multipart')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_create_video_post_missing_video(auth_client, post_list_url):
    data = {
        "content": "Test Post",
        "post_type": "video"
    }
    response = auth_client.post(post_list_url, data, secure=True, format='multipart')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Video posts must include at least one video" in str(response.data)

@pytest.mark.django_db
def test_create_post_invalid(auth_client, post_list_url):
    data = {
        "content": "Test Posting",
        "post_type": "dog",
    }
    response = auth_client.post(post_list_url, data, secure=True, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_get_all_posts(auth_client, post_list_url, populate_posts):
    response = auth_client.get(post_list_url, secure=True, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert Post.objects.count() == 4

@pytest.mark.django_db
def test_get_single_post(auth_client, post_detail_url, populate_posts):
    post1, post2, post3, post4 = populate_posts

    response = auth_client.get(post_detail_url(post3.id), secure=True, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['content'] == post3.content

@pytest.mark.django_db
def test_update_post(post_detail_url, populate_posts, auth_login_client):
    post1, post2, post3, post4 = populate_posts

    login = auth_login_client(post1.author.username, '1234')
    response = login.patch(post_detail_url(post1.id), {"content": "Updated content"}, secure=True, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['content'] != post1.content
    assert response.data['content'] == "Updated content"

@pytest.mark.django_db
def test_update_post_not_author(post_detail_url, populate_posts, auth_login_client):
    post1, post2, post3, post4 = populate_posts

    login = auth_login_client(post4.author.username, '1234')
    response = login.patch(post_detail_url(post1.id), {"content": "I will update you"}, secure=True, format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Post.objects.get(id=post1.id).content == post1.content

@pytest.mark.django_db
def test_delete_post(post_detail_url, populate_posts, auth_login_client):
    post1, post2, post3, post4 = populate_posts

    login = auth_login_client(post1.author.username, '1234')
    response = login.delete(post_detail_url(post1.id), secure=True, format='json')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Post.objects.filter(id=post1.id).exists()

@pytest.mark.django_db
def test_delete_post_not_author(post_detail_url, populate_posts, auth_login_client):
    post1, post2, post3, post4 = populate_posts

    login = auth_login_client(post4.author.username, '1234')
    response = login.delete(post_detail_url(post1.id), secure=True, format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Post.objects.filter(id=post1.id).exists()

@pytest.mark.django_db
def test_like_post(auth_client, like_post_url, populate_posts):
    post1, _, _, _, = populate_posts
    client = auth_client

    like_url = like_post_url(post1.id)

    response  = client.post(like_url, secure=True, format='json')
    user_id = User.objects.get(username='test_user').id

    assert response.status_code == status.HTTP_200_OK
    assert post1.liked_by.filter(id=user_id).exists()

    response_duplicate =  client.post(like_url, secure=True, format='json')
    assert response_duplicate.status_code == status.HTTP_409_CONFLICT

@pytest.mark.django_db
def test_unlike_post(auth_client, like_post_url, populate_posts):
    post1, _, _, _, = populate_posts
    client = auth_client

    like_url = like_post_url(post1.id)
    user_id = User.objects.get(username='test_user').id

    response_like = client.post(like_url, secure=True, format='json')
    assert response_like.status_code == status.HTTP_200_OK
    assert post1.liked_by.filter(id=user_id).exists()

    response_unlike = client.delete(like_url, secure=True, format='json')
    assert response_unlike.status_code == status.HTTP_204_NO_CONTENT
    
    response_unlike_again = client.delete(like_url, secure=True, format='json')
    assert response_unlike_again.status_code == status.HTTP_409_CONFLICT

# Media Validation Tests
@pytest.mark.django_db
def test_post_image_size_validation(auth_client, post_list_url, test_image):
    # Create a large image that exceeds size limit
    large_image = SimpleUploadedFile(
        "large.jpg",
        b"x" * 1024 * 1024 * 11,  # 11MB file
        content_type="image/jpeg"
    )
    
    data = {
        "content": "Test Post with Large Image",
        "post_type": "image",
        "images": [large_image]
    }
    
    response = auth_client.post(post_list_url, data, secure=True, format='multipart')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_post_video_format_validation(auth_client, post_list_url):
    invalid_video = SimpleUploadedFile(
        "test.txt",
        b"invalid video content",
        content_type="text/plain"
    )
    
    data = {
        "content": "Test Post with Invalid Video",
        "post_type": "video",
        "videos": [invalid_video]
    }
    
    response = auth_client.post(post_list_url, data, secure=True, format='multipart')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

# Multiple Media Tests
@pytest.mark.django_db
def test_create_post_with_multiple_images(auth_client, post_list_url):
    # Create two separate image files
    def create_test_image(name):
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(file, 'png')
        file.name = name
        file.seek(0)
        return SimpleUploadedFile(name, file.read(), content_type='image/png')
    
    image1 = create_test_image('test1.png')
    image2 = create_test_image('test2.png')
    
    data = {
        "content": "Test Post with Multiple Images",
        "post_type": "image",
        "images": [image1, image2]
    }
    
    response = auth_client.post(post_list_url, data, secure=True, format='multipart')
    
    if response.status_code != status.HTTP_201_CREATED:
        print("Response data:", response.data)  # Debug info
    
    assert response.status_code == status.HTTP_201_CREATED
    assert Post.objects.count() == 1
    assert Media.objects.count() == 2
    assert len(response.data['post_images']) == 2

# Cleanup Test
@pytest.mark.django_db
def test_media_cleanup_on_post_deletion(auth_client, post_list_url, post_detail_url, mock_post_with_image_data):
    # Create post with image
    response = auth_client.post(post_list_url, mock_post_with_image_data, secure=True, format='multipart')
    post_id = response.data['id']
    
    # Delete post
    delete_response = auth_client.delete(post_detail_url(post_id), secure=True)
    
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    assert Post.objects.count() == 0
    assert Media.objects.count() == 0  # Check if image was also deleted