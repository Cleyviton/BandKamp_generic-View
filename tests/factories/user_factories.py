from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User as UserModel

User: AbstractUser = get_user_model()


def create_user_with_token(user_data=None) -> tuple[UserModel, RefreshToken]:
    if not user_data:
        user_data = {
            "username": "lucira_buster",
            "email": "lucira_buster@kenziebuster.com",
            "full_name": "Lucira",
            "artistic_name": "Buster",
            "password": "1234",
        }

    user = User.objects.create_superuser(**user_data)
    user_token = RefreshToken.for_user(user)

    return user, user_token
