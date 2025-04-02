import pytest
from rest_framework import status
from django.contrib.auth.models import User

from apps.posts.models import Comment


# Test Cases
@pytest.mark.django_db
def test_create_comment(auth_client, comment_list_url, populate_posts, mock_comment_data):
    post1, post2, post3, post4 = populate_posts
    
    response = auth_client.post(comment_list_url(post4.id), mock_comment_data, secure=True, format='json')
    
    comment = response.data
    assert response.status_code == status.HTTP_201_CREATED
    assert comment['content'] == mock_comment_data['content']
    assert Comment.objects.count() == 1

    auth_client.post(comment_list_url(post4.id), mock_comment_data, secure=True, format='json')
    assert Comment.objects.count() == 2

@pytest.mark.django_db
def test_create_comment_invalid(auth_client, comment_list_url, populate_posts):
    post1, post2, post3, post4 = populate_posts
    data = {
        "content": "Test Posting",
        "comment_type": "dog",
    }
    response = auth_client.post(comment_list_url(post4.id), data, secure=True, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

# Comment Image Tests
@pytest.mark.django_db
def test_create_comment_with_image(auth_client, comment_list_url, populate_posts, mock_comment_with_image_data):
    post1, _, _, _ = populate_posts
    
    response = auth_client.post(
        comment_list_url(post1.id), 
        mock_comment_with_image_data, 
        secure=True, 
        format='multipart'
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    assert Comment.objects.count() == 1
    # assert CommentImage.objects.count() == 1
    assert 'comment_image' in response.data
    assert response.data['comment_image'] is not None

@pytest.mark.django_db
def test_create_comment_with_invalid_image(auth_client, comment_list_url, populate_posts, mock_comment_with_invalid_image):
    post1, _, _, _ = populate_posts
    
    response = auth_client.post(
        comment_list_url(post1.id), 
        mock_comment_with_invalid_image, 
        secure=True, 
        format='multipart'
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_create_image_comment_missing_image(auth_client, comment_list_url, populate_posts):
    post1, _, _, _ = populate_posts
    data = {
        "content": "Test Comment",
        "comment_type": "image"
    }
    
    response = auth_client.post(comment_list_url(post1.id), data, secure=True, format='multipart')
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "An image is required." in str(response.data)

@pytest.mark.django_db
def test_media_cleanup_on_comment_deletion(auth_client, comment_list_url, comment_detail_url, mock_comment_with_image_data, populate_posts):
    post1, _, _, _ = populate_posts
    
    # Create comment with image
    response = auth_client.post(
        comment_list_url(post1.id), 
        mock_comment_with_image_data, 
        secure=True, 
        format='multipart'
    )
    comment_id = response.data['id']
    
    # Delete comment
    delete_response = auth_client.delete(
        comment_detail_url(post1.id, comment_id), 
        secure=True
    )
    
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT
    assert Comment.objects.count() == 0
    # assert CommentImage.objects.count() == 0  # Check if image was also deleted

@pytest.mark.django_db
def test_get_all_comments(auth_client, comment_list_url, populate_comments):
    comm1, comm2, comm3, comm4 = populate_comments
    response = auth_client.get(comment_list_url(comm1.post.id), secure=True, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert Comment.objects.count() == 4

@pytest.mark.django_db
def test_get_single_comment(auth_client, comment_detail_url, populate_comments):
    comm1, comm2, comm3, comm4 = populate_comments

    response = auth_client.get(comment_detail_url(comm3.post.id, comm3.id), secure=True, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['content'] == comm3.content

@pytest.mark.django_db
def test_update_comment(comment_detail_url, populate_comments, auth_login_client):
    comm1, comm2, comm3, comm4 = populate_comments

    login = auth_login_client(comm1.author.username, '1234')
    response = login.put(comment_detail_url(comm1.post.id, comm1.id), {"content": "Updated comment"}, secure=True, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['content'] != comm1.content
    assert response.data['content'] == "Updated comment"

@pytest.mark.django_db
def test_update_comment_not_author(comment_detail_url, populate_comments, auth_login_client):
    comm1, comm2, comm3, comm4 = populate_comments

    login = auth_login_client(comm1.author.username, '1234')
    response = login.put(comment_detail_url(comm4.post.id, comm4.id), {"content": "I will update you"}, secure=True, format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Comment.objects.get(id=comm4.id).content == comm4.content

@pytest.mark.django_db
def test_delete_comment(comment_detail_url, populate_comments, auth_login_client):
    comm1, comm2, comm3, comm4 = populate_comments

    login = auth_login_client(comm4.author.username, '1234')
    response = login.delete(comment_detail_url(comm4.post.id, comm4.id), secure=True, format='json')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Comment.objects.filter(id=comm4.id).exists()

@pytest.mark.django_db
def test_cascade_delete_post_comment(post_detail_url, populate_comments, auth_login_client):
    comm1, comm2, comm3, comm4 = populate_comments

    login = auth_login_client(comm4.post.author.username, '1234')
    response = login.delete(post_detail_url(comm4.post.id), secure=True, format='json')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Comment.objects.filter(id=comm4.id).exists()

@pytest.mark.django_db
def test_delete_comment_not_author(comment_detail_url, populate_comments, auth_login_client):
    comm1, comm2, comm3, comm4 = populate_comments

    login = auth_login_client(comm4.author.username, '1234')
    response = login.delete(comment_detail_url(comm3.post.id, comm3.id), secure=True, format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Comment.objects.filter(id=comm3.id).exists()
    
@pytest.mark.django_db
def test_like_comment(auth_client, like_comment_url, populate_posts, populate_comments):
    """Test that a comment can be liked."""
    post1, post2, post3, post4 = populate_posts
    comm1, _, _, _ = populate_comments
    client = auth_client

    like_url = like_comment_url(post1.id, comm1.id)

    response = client.post(like_url, secure=True, format='json')
    try:
        user_id = User.objects.get(username='test_user').id
    except User.DoesNotExist:
        pytest.fail("Test user does not exist")

    # Check that the comment is liked and that the like count is correct
    assert response.status_code == status.HTTP_200_OK
    assert comm1.liked_by.filter(id=user_id).exists()
    assert comm1.liked_by.count() == 1

    # Check that if the comment is already liked, the like count is not increased
    response_duplicate = client.post(like_url, secure=True, format='json')
    assert response_duplicate.status_code == status.HTTP_409_CONFLICT

@pytest.mark.django_db
def test_unlike_comment(auth_client, like_comment_url, populate_posts, populate_comments):
    """Test that a comment can be unliked."""
    post1, post2, post3, post4 = populate_posts
    comm1, _, _, _ = populate_comments
    client = auth_client

    like_url = like_comment_url(post1.id, comm1.id)

    # First, like the comment
    response_like = client.post(like_url, secure=True, format='json')
    assert response_like.status_code == status.HTTP_200_OK

    # Then, unlike the comment and that the like count is correct
    response_unlike = client.delete(like_url, secure=True, format='json')
    assert response_unlike.status_code == status.HTTP_204_NO_CONTENT
    assert comm1.liked_by.count() == 0

    # Finally, try to unlike the comment again and check that it fails
    response_unlike_again = client.delete(like_url, secure=True, format='json')
    assert response_unlike_again.status_code == status.HTTP_409_CONFLICT
