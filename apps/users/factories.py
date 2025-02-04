from django.contrib.auth.models import User, Group

from apps.users.models import Profile


class UserFactory:

    @staticmethod
    def create_user_and_profile(username, email, password, first_name, last_name, bio=""):
        if username is None or email is None or password is None or first_name is None or last_name is None:
            raise ValueError("Username, email, password and first_name and last_name are required")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        profile = Profile.objects.create(user=user, first_name=first_name, last_name=last_name, bio=bio)
        return profile

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