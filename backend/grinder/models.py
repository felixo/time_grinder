from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Application user, defined before the initial database migration."""
