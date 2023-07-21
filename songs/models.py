from django.db import models


class Song(models.Model):
    class Meta:
        ordering = ("id",)

    title = models.CharField(max_length=255)
    duration = models.CharField(max_length=255)

    album = models.ForeignKey(
        "albums.Album",
        on_delete=models.CASCADE,
        related_name="songs",
    )
