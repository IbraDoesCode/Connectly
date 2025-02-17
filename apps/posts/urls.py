from django.urls import path
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/comments/', CommentListView.as_view(), name='comment_list'),
    path('<int:post_id>/comments/<int:comment_id>/', CommentDetailView.as_view(), name='comment_detail'),
    path('<int:post_id>/like/', LikePostView.as_view(), name='like_post'),
    path('<int:post_id>/comments/<int:comment_id>/like/', LikeCommentView.as_view(), name='like_comment')
]
