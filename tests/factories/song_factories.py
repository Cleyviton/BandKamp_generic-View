from songs.models import Song
from django.contrib.auth.models import AbstractUser
from .album_factories import create_album_with_user
from django.db.models import QuerySet
from albums.models import Album


def create_song_with_album(
    user: AbstractUser,
    song_data: dict = None,
    album: Album = None,
) -> Song:

    if not album:
        album = create_album_with_user(user)

    if not song_data:
        song_data = {
            "title": "Unreachable",
            "duration": "110min",
        }

    song = Song.objects.create(**song_data, album=album)

    return song


def create_multiple_songs_with_album(
    user: AbstractUser,
    songs_count: int,
    album: Album = None,
) -> QuerySet[Album]:

    if not album:
        album = create_album_with_user(user=user)

    songs_data = [
        {
            "title": f"Song {index}",
            "duration": f"1{index}",
            "album": album,
        }
        for index in range(1, songs_count + 1)
    ]
    song_objects = [Song(**song_data) for song_data in songs_data]
    songs = Song.objects.bulk_create(song_objects)

    return songs
