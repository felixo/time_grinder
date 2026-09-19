from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Time Grinder user, kept minimal so account behavior can evolve later."""
