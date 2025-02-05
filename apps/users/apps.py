from django.apps import AppConfig
from utils.logger import Logger


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'

    def ready(self):
        self.create_groups()

    # This method initializes the group thingy for role_based access
    def create_groups(self):
        from django.contrib.auth.models import Group

        logger = Logger().get_logger()
        admin_group, created_admin = Group.objects.get_or_create(name='Admin')
        moderator_group, created_mod = Group.objects.get_or_create(name='Moderator')

        if created_admin and created_mod:
            logger.info("Groups created: Admin and Moderator")
        else:
            logger.info("Groups already exist: Admin and Moderator")