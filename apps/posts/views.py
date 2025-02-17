# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from utils.response_factory import ResponseFactory
from .models import Post, Comment
from .permissions import IsAuthor, IsOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer


# Post List View (GET all posts, POST new post)
class PostListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        # Get all posts
        posts = Post.objects.all()
        # Convert QuerySet to JSON
        serializer = PostSerializer(posts, many=True)
        # Return JSON data
        return ResponseFactory.success(serializer.data,serializer.data)

    def post(self, request):
        # Take the data from the request and convert it to JSON
        serializer = PostSerializer(data=request.data)

        # Check if the data is valid
        if not serializer.is_valid():
            # If the data is not valid, return an error
            return ResponseFactory.bad_request(
                f"Error creating post",
                serializer.errors
            )

        # Save the data to the database
        post = serializer.save(author=self.request.user)

        # Return the JSON data
        return ResponseFactory.created(
            f"Post {post} created successfully",
            serializer.data
        )

# Post Detail View (GET, PUT, DELETE a single post)
class PostDetailView(APIView):
    serializer_class = PostSerializer

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, post_id):
        try:
            # Get specific post based on id
            post = Post.objects.get(id=post_id)

            # Serialize the post object
            serializer = PostSerializer(post)

            # Return the serialized JSON to http response
            return ResponseFactory.success(
                serializer.data,
                serializer.data
            )
        except Post.DoesNotExist:
            # Throw an error if the post with the specified id is not found
            return ResponseFactory.not_found(
                f"Post {post_id} not found",
                {'Message': 'Post not found'}
            )

    def patch(self, request, post_id):
        try:
            # Get specified post based on primary key
            post = Post.objects.get(id=post_id)

            # Check authentication and permissions
            self.check_object_permissions(request, post)

            # Update the post using the serializer
            serializer = PostSerializer(post, data=request.data, partial=True)

            # Check if the serializer is valid, raise exception if the request data contains invalid field
            if not serializer.is_valid():
                # Return a bad request if there are other errors
                return ResponseFactory.bad_request(
                    f"Error updating post",
                    serializer.errors
                )

            # Save the serializer data to the db
            serializer.save()
            print(serializer.data)
            # Return an ok response
            return ResponseFactory.success(
                f"Post updated successfully",
                serializer.data
            )

        except Post.DoesNotExist:
            # Throw an error if the post is not found
            return ResponseFactory.not_found(
                "Update Error: Post not found",
                {'Message': 'Post not found'}
            )

    def delete(self, request, post_id):
        try:
            # Get specified post based on primary key
            post = Post.objects.get(pk=post_id)

            # Check authentication and permissions
            self.check_object_permissions(request, post)

            # Delete the post from the db
            post.delete()

            # Return an ok response
            return ResponseFactory.deleted(
                "Post deleted successfully",
                {'Message': 'Post deleted successfully'}
            )
        except Post.DoesNotExist:
            # Throw an error if the post with the specified id is not found
            return ResponseFactory.not_found(
                "Error deleting post",
                {'Message': 'Post not found'}
            )

# Comment List View for a specific post
class CommentListView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            # Check if the post exists
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return ResponseFactory.not_found(
                "Error: Post not found",
                {'Message': 'Post not found'}
            )
        
        # Get all comments for the post
        comments = post.comments.all()
        
        # Convert QuerySet to JSON
        serializer = CommentSerializer(comments, many=True)
        
        # Return JSON data
        return ResponseFactory.success(
            serializer.data,
            serializer.data
        )

    def post(self, request, post_id):
        try:
            # Check if the post exists
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return ResponseFactory.not_found(
                "Create Error: Post not found",
                {'Message': 'Post not found'}
            )
        
        # Take the data from the request and convert it to JSON
        serializer = CommentSerializer(data=request.data)
        
        # Check if the data is valid
        if serializer.is_valid():
            # Save the data to the database
            serializer.save(post=post, author=self.request.user)

            # Return the JSON data
            return ResponseFactory.created(
                "Comment created successfully",
                serializer.data
            )

        # If the data is not valid, return an error
        return ResponseFactory.bad_request(
            f"Error creating comment {serializer.errors}",
            serializer.errors
        )

# Comment Detail View (GET, PUT, DELETE a specific comment)
class CommentDetailView(APIView):
    serializer_class = CommentSerializer

    # Overrides the permission to allow GET of a single post even if the user is not the author
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAuthor()]

    def get(self, request, post_id, comment_id):
        try:
            # Check if the post exists
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return ResponseFactory.not_found(
                "Post not found",
                {'Message': 'Post not found'}
            )

        try:
            # Get the specific comment for the post
            comment = post.comments.get(pk=comment_id)
        except Comment.DoesNotExist:
            return ResponseFactory.not_found(
                "Comment not found",
                {'Message': 'Comment not found'}
            )

        # Serialize and return the comment
        serializer = CommentSerializer(comment)
        return ResponseFactory.success(
            serializer.data,
            serializer.data
        )

    def put(self, request, post_id, comment_id):
        try:
            # Check if the post exists
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return ResponseFactory.not_found(
                "Update Error: Post not found",
                {'Message': 'Post not found'}
            )

        try:
            # Get the specific comment for the post
            comment = post.comments.get(pk=comment_id)
        except Comment.DoesNotExist:
            return ResponseFactory.not_found(
                "Update Error: Comment not found",
                {'Message': 'Comment not found'}
            )

        # Check authentication and permissions
        self.check_object_permissions(request, comment)

        # Deserialize and update the comment
        serializer = CommentSerializer(comment, data=request.data)
        
        if serializer.is_valid():
            serializer.save()

            return ResponseFactory.success(
                "Comment updated successfully",
                serializer.data
            )

        # If data is invalid, return errors
        return ResponseFactory.bad_request(
            "Error updating comment",
            serializer.errors
        )

    def delete(self, request, post_id, comment_id):
        try:
            # Check if the post exists
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return ResponseFactory.not_found(
                "Delete Error: Post not found",
                {'Message': 'Post not found'}
            )

        try:
            # Get the specific comment for the post
            comment = post.comments.get(pk=comment_id)
        except Comment.DoesNotExist:
            return ResponseFactory.not_found(
                "Delete Error: Comment does not exist",
                {'Message': 'Comment not found'}
            )
        
        # Check authentication and permissions
        self.check_object_permissions(request, comment)

        # Delete the comment
        comment.delete()
        return ResponseFactory.deleted(
            "Comment deleted successfully",
            {'Message': 'Comment deleted successfully'}
        )

class LikePostView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        # Find post by post_id
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return ResponseFactory.not_found('Post not found', 
                                             {'message': 'Post not found'})

        # Check if the user already liked the post
        user = request.user
        #if not liked, add user to liked_by
        if not post.liked_by.filter(id=user.id).exists():
            post.liked_by.add(user)
        #if liked, return message post already liked
        else:
            return ResponseFactory.conflict('Post already liked',
                                             {'message': 'Post already liked'})

        # Return Success response with updated like count
        like_count = post.liked_by.count()   
        return ResponseFactory.success('Post successfully liked',
                                        {'message': 'Post successfully liked',
                                        'like_count': like_count})

    def delete(self, request, post_id):
        # Find post by post_id
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return ResponseFactory.not_found('Post not found', 
                                             {'message': 'Post not found'})

        # Check if the user already liked the post
        user = request.user
        # if  liked, remove user from liked_by
        if post.liked_by.filter(id=user.id).exists():
            post.liked_by.remove(user)
        # if not liked, return message post not liked
        else:
            return ResponseFactory.conflict('Post not liked',
                                             {'message': 'Post not liked'})

        # Return success response with updated like count
        like_count = post.liked_by.count()
        return ResponseFactory.deleted('Post unliked', 
                                       {'message': 'Post unliked',
                                        'like_count': like_count})
class LikeCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return ResponseFactory.not_found('Comment not found', 
                                             {'message': 'Comment not found'})

        if comment is None:
            return ResponseFactory.not_found('Comment not found', 
                                             {'message': 'Comment not found'})

        user = request.user
        if comment.liked_by.filter(id=user.id).exists():
            return ResponseFactory.conflict('Comment already liked', 
                                            {'message': 'Comment already liked'})

        comment.liked_by.add(user)
        like_count = comment.liked_by.count()
        return ResponseFactory.success('Comment successfully liked',
                                       {'message': 'Comment successfully liked',
                                        'like_count': like_count})

    def delete(self, request, post_id, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return ResponseFactory.not_found('Comment not found', 
                                             {'message': 'Comment not found'})

        if comment is None:
            return ResponseFactory.not_found('Comment not found', 
                                             {'message': 'Comment not found'})

        user = request.user
        if not comment.liked_by.filter(id=user.id).exists():
            return ResponseFactory.conflict('Comment not liked', 
                                            {'message': 'Comment not liked'})

        comment.liked_by.remove(user)
        like_count = comment.liked_by.count()
        return ResponseFactory.deleted('Comment unliked', 
                                       {'message': 'Comment unliked',
                                        'like_count': like_count})

