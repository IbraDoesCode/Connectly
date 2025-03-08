import pytest
from rest_framework import status


@pytest.mark.django_db
def test_follow_user_successfully(auth_login_client, populate_users, follow_url):
    user1, user2, _ = populate_users
    client = auth_login_client(user1.user.username, '1234')

    response = client.post(follow_url(user2.user.id), secure=True)
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_user_cannot_follow_themselves(auth_login_client, populate_users, follow_url):
    user1, _, _ = populate_users
    client = auth_login_client(user1.user.username, '1234')

    response = client.post(follow_url(user1.user.id), secure=True)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_follow_user_not_found(auth_login_client, populate_users, follow_url):
    user1, _, _ = populate_users
    client = auth_login_client(user1.user.username, '1234')

    # Pass non existing id
    response = client.post(follow_url("20"),secure=True)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_unfollow_user_successfully(auth_login_client, populate_users, follow_url):
    user1, user2, _ = populate_users
    client = auth_login_client(user1.user.username, '1234')

    #Follow
    response = client.post(follow_url(user2.user.id), secure=True)
    assert response.status_code == status.HTTP_201_CREATED

    #Unfollow
    unfollow_response = client.post(follow_url(user2.user.id), secure=True)
    assert unfollow_response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_get_user_followers(auth_login_client, populate_users, follow_url):
    user1, user2, _ = populate_users
    client = auth_login_client(user1.user.username, '1234')

    response = client.post(follow_url(user2.user.id), secure=True)
    assert response.status_code == status.HTTP_201_CREATED

    followers_response = client.get(follow_url(user2.user.id, query_kwargs={'type': 'follower'}), secure=True)
    assert followers_response.status_code == status.HTTP_200_OK
    assert followers_response.data[0]['id'] == user1.user.id


@pytest.mark.django_db
def test_get_user_following(auth_login_client, populate_users, follow_url):
    user1, user2, _ = populate_users
    client = auth_login_client(user1.user.username, '1234')

    response = client.post(follow_url(user2.user.id), secure=True)
    assert response.status_code == status.HTTP_201_CREATED

    followers_response = client.get(follow_url(user1.user.id, query_kwargs={'type': 'following'}), secure=True)
    assert followers_response.status_code == status.HTTP_200_OK
    assert followers_response.data[0]['id'] == user2.user.id