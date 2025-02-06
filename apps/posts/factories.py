from apps.posts.models import Post, Comment


class PostFactory:
    @staticmethod
    def create_post(author, post_type, content='', metadata=None):
        if post_type not in dict(Post.POST_TYPES):
            raise ValueError('Invalid post type')

        # Add validation for specific types
        if post_type == 'image' and 'file_size' not in metadata:
            raise ValueError("Image posts require 'file_size' in metadata")
        if post_type == 'video' and 'duration' not in metadata:
            raise ValueError("Video posts require 'duration' in metadata")

        return Post.objects.create(
            author=author,
            post_type=post_type,
            content=content,
            metadata=metadata,
        )

class CommentFactory:
    @staticmethod
    def create_comment(post, author, comment_type, content='', metadata=None):
        if comment_type not in dict(Post.POST_TYPES):
            raise ValueError('Invalid post type')

        # Add validation for specific types
        if comment_type == 'image' and 'file_size' not in metadata:
            raise ValueError("Image posts require 'file_size' in metadata")

        return Comment.objects.create(
            post=post,
            author=author,
            comment_type=comment_type,
            content=content,
            metadata=metadata,
        )