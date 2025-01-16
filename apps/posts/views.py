# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# Post List View (GET all posts)
class PostListView(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass
# Post Detail View (GET, PUT, DELETE a single post)
class PostDetailView(APIView):
    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass

# Comment List View for a specific post
class CommentListView(APIView):
    def get(self, request, post_id):
        pass

    def post(self, request, post_id):
        pass

# Comment Detail View (GET, PUT, DELETE a specific comment)
class CommentDetailView(APIView):
    def get(self, request, post_id, comment_id):
        pass

    def put(self, request, post_id, comment_id):
        pass

    def delete(self, request, post_id, comment_id):
        pass
