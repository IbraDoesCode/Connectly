from django.contrib.auth.models import User, Group
from rest_framework.exceptions import ValidationError
from apps.users.models import Profile


class UserFactory:
    # * Highlighted comments means it was modified
    @staticmethod
    def create_user_and_profile(username, email, password, first_name, last_name, bio=""):
        
        # * Looks through the fields with missing values
        missing_fields = {k: v for k, v in locals().items() if not v and k not in ['bio']} 

        # * Uses the missing fields to raise an error
        # * It makes the more descriptive and readable on what fields are exactly missing
        if missing_fields:
            ''' * Raise a ValidationError instead of ValueError, since ValueError won’t be caught properly by DRF, 
                    this way it would still return a proper response rather than crashing the server '''
            raise ValidationError({k: "This field is required." for k in missing_fields})
        
        # Check if the username already exists before trying to create the user
        if User.objects.filter(username=username).exists():
            raise ValidationError({"username": "This username is already taken."})
        
        # Check if the email already exists before trying to create the user
        if User.objects.filter(email=email).exists():
            raise ValidationError({"email": "This email is already in use."})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return Profile.objects.create(user=user, first_name=first_name, last_name=last_name, bio=bio)
    
    @staticmethod
    def create_profile_for_existing_user(user):
        """
        Creates a Profile for an already existing User (Google OAuth users).
        """
        if Profile.objects.filter(user=user).exists():
            return Profile.objects.get(user=user)  # Return existing profile if already created

        # Ensure first_name and last_name are set
        first_name = user.first_name if user.first_name else ""
        last_name = user.last_name if user.last_name else ""

        return Profile.objects.create(user=user, first_name=first_name, last_name=last_name, bio="")

    @staticmethod
    def assign_user_role(user, role):
        user.groups.clear()
        group = Group.objects.get(name=role)
        user.groups.add(group)

    @staticmethod
    def create_admin_user(username, email, password, first_name, last_name, bio=""):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        profile = Profile.objects.create(user=user, first_name=first_name, last_name=last_name, bio=bio)
        UserFactory.assign_user_role(user, role='Admin')
        return profile