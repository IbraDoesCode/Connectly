# Create your views here.
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.medias.models import Media
from django.contrib.contenttypes.models import ContentType
from utils.response_factory import ResponseFactory
from .models import Post, Comment
from ..users.models import Follow
from .permissions import IsAuthor, IsOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer
from rest_framework.generics import ListAPIView


# Post List View (GET all posts, POST new post)
class PostListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        following = Follow.objects.filter(follower=user).values_list('followed', flat=True)

        posts = Post.objects.filter(
            Q(privacy_type='public') |
            Q(author=user) |
            Q(author__id__in=following, privacy_type='followers')
        ).order_by('-created_at')

        return posts

    def get(self, request, *args, **kwargs):
        # Get the queryset and paginate it manually
        posts = self.paginate_queryset(self.get_queryset()) # Apply pagination
        
        # Serialize the paginated queryset
        serializer = PostSerializer(posts, many=True, context={'request': request})
        
        # Return the paginated response (with pagination metadata like 'next', 'previous')
        return ResponseFactory.success(serializer.data, self.get_paginated_response(serializer.data).data)

    def post(self, request):
        # Take the data from the request and convert it to JSON
        serializer = PostSerializer(data=request.data, context={'request': request})

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

            if post.author != request.user:
                if post.privacy_type == 'private':
                    return ResponseFactory.forbidden('Access Denied', {'detail': 'You do not have access to this post'})
            
                if post.privacy_type == 'followers':
                    is_following = Follow.objects.filter(follower=request.user, followed=post.author).exists()
                    if not is_following:
                        return ResponseFactory.forbidden('Access Denied', {'detail': 'You do not have access to this post'})
            
            # Serialize the post object
            serializer = PostSerializer(post, context={'request': request})

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
            serializer = PostSerializer(post, data=request.data, partial=True, context={'request': request})

            # Check if the serializer is valid, raise exception if the request data contains invalid field
            if not serializer.is_valid():
                # Return a bad request if there are other errors
                return ResponseFactory.bad_request(
                    f"Error updating post",
                    serializer.errors
                )

            # Save the serializer data to the db
            serializer.save()

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
            post = Post.objects.get(pk=post_id)
            self.check_object_permissions(request, post)

            # Delete associated media files before deleting the post
            media = Media.objects.filter(content_type=ContentType.objects.get_for_model(post), object_id=post.id)
            for media_file in media:
                media_file.file.delete(save=False)  # Deleting the file from the storage

            #delete the media records from the database
            media.delete()

            # Delete the post itself
            post.delete()

            return ResponseFactory.deleted("Post deleted successfully", {'Message': 'Post deleted successfully'})

        except Post.DoesNotExist:
            return ResponseFactory.not_found("Error deleting post", {'Message': 'Post not found'})

# Comment List View for a specific post
class CommentListView(ListAPIView):
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
        comments = self.paginate_queryset(post.comments.all().order_by('-created_at')) # Apply pagination
        
        # Convert QuerySet to JSON
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        
        # Return JSON data
        return ResponseFactory.success(serializer.data, self.get_paginated_response(serializer.data).data)

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
        serializer = CommentSerializer(data=request.data, context={'request': request})
        
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
        serializer = CommentSerializer(comment, context={'request': request})
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
        serializer = CommentSerializer(comment, data=request.data, context={'request': request})
        
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
            message = 'Post liked successfully'
        #if post liked, remove the user from liked_by
        else:
            post.liked_by.remove(user)
            message = 'Post unliked successfully'

        # Return Success response with updated like count
        like_count = post.liked_by.count()   
        return ResponseFactory.success(message,
                                        {'detail': message,
                                        'like_count': like_count})


class LikeCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return ResponseFactory.not_found('Comment not found', 
                                             {'message': 'Comment not found'})
        
        user = request.user
        if comment.liked_by.filter(id=user.id).exists():
            comment.liked_by.remove(user)
            message = 'Comment unliked successfully'
        else:
            comment.liked_by.add(user)
            message = 'Comment liked successfully'
        
        liked = comment.liked_by.filter(id=user.id).exists()
        return ResponseFactory.success(message,
                                        {'detail': message,
                                        'liked': liked})
