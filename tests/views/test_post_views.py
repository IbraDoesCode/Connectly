import pytest
from rest_framework import status
from django.contrib.auth.models import User
from apps.posts.models import Post


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
