# import pytest
# from rest_framework import status
# import time

# @pytest.mark.django_db
# def test_anon_rate_limiting(api_client, token_login_url, mock_user_data):
#     """Test anonymous user rate limiting"""
#     # Use login endpoint which allows anonymous access
#     test_data = {
#         'username': mock_user_data['username'],
#         'password': mock_user_data['password']
#     }
    
#     # Make multiple requests quickly
#     for _ in range(11):  # One more than the limit
#         response = api_client.post(token_login_url, test_data, secure=True)
    
#     # Last request should be throttled (anon: 10/minute)
#     assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
#     assert 'Request was throttled' in str(response.content)

# @pytest.mark.django_db
# def test_user_rate_limiting(auth_client, post_list_url):
#     """Test authenticated user rate limiting"""
#     # Make requests faster than allowed (user: 2/second)
#     for _ in range(3):  # Third request should be throttled
#         response = auth_client.get(post_list_url, secure=True, format='json')
    
#     assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
#     assert 'Request was throttled' in str(response.content)
    
# @pytest.mark.django_db
# def test_rate_limit_reset(auth_client, post_list_url):
#     """Test that rate limits reset after waiting"""
#     # Make initial requests
#     for _ in range(2):
#         auth_client.get(post_list_url, secure=True)
    
#     # Wait for rate limit to reset (>1 second)
#     time.sleep(1.1)
    
#     # Should be able to make requests again
#     response = auth_client.get(post_list_url, secure=True)
#     assert response.status_code == status.HTTP_200_OK
    
# @pytest.mark.django_db
# def test_different_endpoints(auth_client, post_list_url, get_all_users_url):
#     """Test that rate limits apply across different endpoints"""
#     # Make requests to different endpoints
#     for _ in range(3):
#         if _ % 2 == 0:
#             response = auth_client.get(post_list_url, secure=True)
#         else:
#             response = auth_client.get(get_all_users_url, secure=True)
    
#     assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS

# @pytest.mark.django_db
# def test_throttle_methods(auth_client, post_list_url, mock_post_data):
#     """Test that rate limits apply to different HTTP methods"""
#     # Mix GET and POST requests
#     auth_client.get(post_list_url, secure=True)
#     auth_client.post(post_list_url, mock_post_data, secure=True)
#     response = auth_client.get(post_list_url, secure=True)
    
#     assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS