# Create your views here.
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# Post List View (GET all posts)
class PostListView(APIView):
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
    def get(self, request, pk):
        try:
            # Get specific post based on primary key
            post = Post.objects.get(pk=pk)
            # Serialize the post object
            serializer = PostSerializer(post)
            # Return the serialized JSON to http response
            return Response(serializer.data)
        except Post.DoesNotExist:
            # Throw an error if the post with the specified id is not found
            return Response({'Message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            # Get specified post based on primary key
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            # Throw an error if the post is not found
            return Response({'Message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update the post using the serializer
        serializer = PostSerializer(post, data=request.data, partial=True)

        try:
            # Check if the serializer is valid, raise exception if the request data contains invalid field
            if serializer.is_valid(raise_exception=True):
                # Save the serializer data to the db
                serializer.save()
                # Return an ok response
                return Response(f"Post has been updated successfully, {serializer.data}", status=status.HTTP_200_OK )
            else:
                # Return a bad request if there are other errors
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            # Return a response to the ValidationError that was raised
            return Response(e.messages, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        try:
            # Get specified post based on primary key
            post = Post.objects.get(pk=pk)
            # Delete the post from the db
            post.delete()
            # Return an ok response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            # Throw an error if the post with the specified id is not found
            return Response({'Message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

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
