import pytest
from rest_framework import status

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