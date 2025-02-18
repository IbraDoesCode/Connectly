from apps.posts.models import Post, Comment


class PostFactory:
    @staticmethod
    def create_post(author, post_type, content=''):
        if post_type not in dict(Post.POST_TYPES):
            raise ValueError('Invalid post type')

        return Post.objects.create(
            author=author,
            post_type=post_type,
            content=content,
        )

class CommentFactory:
    @staticmethod
    def create_comment(post, author, comment_type, content=''):
        if comment_type not in dict(Post.POST_TYPES):
            raise ValueError('Invalid post type')


        return Comment.objects.create(
            post=post,
            author=author,
            comment_type=comment_type,
            content=content
        )