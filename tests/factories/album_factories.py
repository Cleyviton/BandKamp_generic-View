from albums.models import Album
from django.contrib.auth.models import AbstractUser
from .user_factories import create_user_with_token
from django.db.models import QuerySet


def create_album_with_user(
    user: AbstractUser,
    album_data: dict = None,
) -> Album:

    if not album_data:
        album_data = {
            "name": "Shadows Collide with People",
            "year": 2000,
        }

    album = Album.objects.create(**album_data, user=user)

    return album


def create_multiple_albums_with_user(
    user: AbstractUser, albums_count: int
) -> QuerySet[Album]:
    albums_data = [
        {
            "name": f"Algum {index}",
            "year": 1993,
            "user": user,
        }
        for index in range(1, albums_count + 1)
    ]
    albums_objects = [Album(**album_data) for album_data in albums_data]
    albums = Album.objects.bulk_create(albums_objects)

    return albums
