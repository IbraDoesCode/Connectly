# Create your views here.
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthor


# Post List View (GET all posts)
class PostListView(APIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated, IsAuthor]

    def get(self, request, pk):
        try:
            # Get specific post based on primary key
            post = Post.objects.get(pk=pk)
            # Check authentication and permissions
            self.check_object_permissions(request, post)
            # Serialize the post object
            serializer = PostSerializer(post)
            # Return the serialized JSON to http response
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
                # Check authentication and permissions
                self.check_object_permissions(request, post)
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
            # Check authentication and permissions
            self.check_object_permissions(request, post)
            # Delete the post from the db
            post.delete()
            # Return an ok response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            # Throw an error if the post with the specified id is not found
            return Response({'Message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

# Comment List View for a specific post
class CommentListView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            # Check if the post exists
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'Message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get all comments for the post
        comments = Comment.objects.filter(post_id=post_id)
        
        # Check if there are any comments
        if not comments.exists():
            return Response({'Message': 'No comments found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Convert QuerySet to JSON
        serializer = CommentSerializer(comments, many=True)
        
        # Return JSON data
        return Response(serializer.data)

    def post(self, request, post_id):
        try:
            # Check if the post exists
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'Message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Take the data from the request and convert it to JSON
        serializer = CommentSerializer(data=request.data)
        
        # Check if the data is valid
        if serializer.is_valid():
            # Save the data to the database
            serializer.save(post=post, author=request.user)
            # Return the JSON data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # If the data is not valid, return an error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Comment Detail View (GET, PUT, DELETE a specific comment)
class CommentDetailView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get(self, request, post_id, comment_id):
        try:
            # Check if the post exists
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'Message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Get the specific comment for the post
            comment = Comment.objects.get(pk=comment_id, post=post)
        except Comment.DoesNotExist:
            return Response({'Message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and return the comment
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, post_id, comment_id):
        try:
            # Check if the post exists
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'Message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Get the specific comment for the post
            comment = Comment.objects.get(pk=comment_id, post=post)
        except Comment.DoesNotExist:
            return Response({'Message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check authentication and permissions
        self.check_object_permissions(request, comment)

        # Deserialize and update the comment
        serializer = CommentSerializer(comment, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If data is invalid, return errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, comment_id):
        try:
            # Check if the post exists
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'Message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Get the specific comment for the post
            comment = Comment.objects.get(pk=comment_id, post=post)
        except Comment.DoesNotExist:
            return Response({'Message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check authentication and permissions
        self.check_object_permissions(request, comment)

        # Delete the comment
        comment.delete()
        return Response({'Message': 'Comment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
