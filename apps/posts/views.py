# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# Post List View (GET all posts)
class PostListView(APIView):
    serializer_class = PostSerializer

    def get(self, request):
        # Get all posts
        posts = Post.objects.all()
        # Convert QuerySet to JSON
        serializer = PostSerializer(posts, many=True)
        # Return JSON data
        return Response(serializer.data)

    def post(self, request):
        # Take the data from the request and convert it to JSON
        serializer = PostSerializer(data=request.data)
        # Check if the data is valid
        if serializer.is_valid():
            # Save the data to the database
            serializer.save()
            # Return the JSON data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If the data is not valid, return an error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Post Detail View (GET, PUT, DELETE a single post)
class PostDetailView(APIView):
    serializer_class = PostSerializer

    def get(self, request, pk):
        pass

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        pass

# Comment List View for a specific post
class CommentListView(APIView):
    serializer_class = CommentSerializer

    def get(self, request, post_id):
        pass

    def post(self, request, post_id):
        pass

# Comment Detail View (GET, PUT, DELETE a specific comment)
class CommentDetailView(APIView):
    serializer_class = CommentSerializer

    def get(self, request, post_id, comment_id):
        pass

    def put(self, request, post_id, comment_id):
        pass

    def delete(self, request, post_id, comment_id):
        pass
