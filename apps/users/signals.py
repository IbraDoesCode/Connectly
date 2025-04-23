import os
from django.db import IntegrityError
from django.db.models.signals import post_migrate
from django.contrib.auth.models import User, Group
from apps.users.factories import UserFactory
from apps.users.models import Profile
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.serializers import UserSerializer
from utils.logger import Logger
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
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

@receiver(post_migrate)
def create_google_oauth_app(sender, **kwargs):
    if sender.name == "allauth":
        try:
            # Ensure localhost exists
            site_localhost, _ = Site.objects.get_or_create(domain="localhost", defaults={"name": "Localhost"})
            # Ensure 127.0.0.1 exists
            site_127, _ = Site.objects.get_or_create(domain="127.0.0.1", defaults={"name": "Localhost (127.0.0.1)"})

            # Create Google OAuth Social Application
            google_app, created = SocialApp.objects.get_or_create(
                provider="google",
                name="Google OAuth",
                defaults={
                    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                    "secret": os.getenv("GOOGLE_CLIENT_SECRET")
                },
            )

            # Assign both sites to the Google OAuth app
            google_app.sites.add(site_localhost, site_127)

            if created:
                logger.info("✅ Google OAuth Social Application created successfully")
            else:
                logger.info("Google OAuth Social Application already exists")

        except IntegrityError as e:
            logger.error(f"Database integrity error while creating Google OAuth App: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while creating Google OAuth App: {e}")
            
@receiver(user_signed_up)
def create_user_profile(user, **kwargs):
    """
    Signal triggered when a user logs in via Google OAuth.
    Calls UserFactory to ensure a Profile is created.
    """
    UserFactory.create_profile_for_existing_user(user)
    