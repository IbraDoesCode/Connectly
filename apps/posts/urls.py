from django.urls import path
from .views import PostListView, PostDetailView, CommentListView, CommentDetailView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:post_id>/comments/', CommentListView.as_view(), name='comment_list'),
    path('posts/<int:post_id>/comments/<int:comment_id>/', CommentDetailView.as_view(), name='comment_detail'),
]
