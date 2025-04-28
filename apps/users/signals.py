import os
from django.db import IntegrityError
from django.db.models.signals import post_migrate
from django.contrib.auth.models import User, Group
from apps.users.models import Profile
from django.dispatch import receiver
from utils.logger import Logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = Logger().get_logger()
    
"""
Signal receiver that creates default user groups after migrations.
    
Annotation:
    @receiver: Decorates the function as a signal receiver.
    post_migrate: Connects the function to the 'post_migrate' signal. Ensures the function runs after migrations.
"""
@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name == "apps.users":
        try:
            # Ensure get_or_create() always returns a tuple
            admin_group, created_admin = Group.objects.get_or_create(name="Admin")
            mod_group, created_mod = Group.objects.get_or_create(name="Moderator")

            if created_admin or created_mod:
                logger.info("✅ Groups created: Admin and/or Moderator")
            else:
                logger.info("ℹ️ Groups already exist: Admin and Moderator")

        except IntegrityError as e:
            logger.error(f"❌ Database integrity error while creating groups: {e}")
        except Exception as e:
            logger.error(f"❌ Unexpected error while creating groups: {e}")
            
# ! THIS SHOULD ONLY BE ENABLED ON DEVELOPMENT
    """
    Signal receiver that creates a default admin user after migrations.
    
    Annotation:
        @receiver: Decorates the function as a signal receiver.
        post_migrate: Connects the function to the 'post_migrate' signal. Ensures the function runs after migrations.
    """
@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    if sender.name == "apps.users":
        try:
            # Ensure the 'Admin' group exists before proceeding
            admin_group, _ = Group.objects.get_or_create(name="Admin")

            result = User.objects.get_or_create(
                username="admin",
                defaults={
                    "email": "admin@super.com",
                    "is_staff": True,
                    "is_superuser": True,
                },
            )

            # Ensure result is a tuple before unpacking
            if isinstance(result, tuple) and len(result) == 2:
                admin_user, created_admin = result
            else:
                raise ValueError("get_or_create() did not return the expected tuple")

            if created_admin:
                admin_user.set_password("admin1234")  # Set password separately
                admin_user.save()

                # Ensure Profile exists
                Profile.objects.get_or_create(
                    user=admin_user, first_name="admin", last_name="super", bio=""
                )

                # Assign the Admin group
                admin_user.groups.add(admin_group)

                logger.info("✅ Default Admin User created successfully")
            else:
                logger.info("ℹ️ Default Admin User already exists")

        except Exception as e:
            logger.error(f"❌ Error creating default admin: {e}")

    