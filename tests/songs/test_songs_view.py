from rest_framework.test import APITestCase
from rest_framework.views import status
from tests.factories import (
    create_user_with_token,
    create_album_with_user,
    create_multiple_songs_with_album,
)
import ipdb


class SongViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user, token = create_user_with_token()
        cls.access_token = str(token.access_token)

        cls.album = create_album_with_user(user=cls.user)

        cls.BASE_URL = f"/api/albums/{cls.album.pk}/songs/"

        # UnitTest Longer Logs
        cls.maxDiff = None

    def test_songs_listing_pagination(self):
        songs_count = 10
        create_multiple_songs_with_album(
            user=self.user, songs_count=songs_count, album=self.album
        )

        response = self.client.get(self.BASE_URL)
        resulted_data = response.json()

        # RETORNO CHAVES
        resulted_pagination_keys = set(resulted_data.keys())
        expected_pagination_keys = {"count", "next", "previous", "results"}
        msg = "Verifique se a paginação está sendo feita corretamente"
        self.assertSetEqual(expected_pagination_keys, resulted_pagination_keys)

        # TAMANHO DO RETORNO
        results_len = len(resulted_data["results"])
        expected_len = 2
        msg = (
            "Verifique se a paginação está retornando apenas "
            + f"{expected_len} items de cada vez no GET em {self.BASE_URL}"
        )
        self.assertEqual(expected_len, results_len, msg)

    def test_song_creation_without_required_fields(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.post(self.BASE_URL, data={}, format="json")

        resulted_data: dict = response.json()

        # RETORNO CHAVES JSON
        expected_fields = {"title", "duration"}
        returned_fields = set(resulted_data.keys())
        msg = "Verifique se todas as chaves obrigatórias são retornadas ao tentar criar uma música sem dados"
        self.assertSetEqual(expected_fields, returned_fields, msg)

        # STATUS CODE
        expected_status_code = status.HTTP_400_BAD_REQUEST
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST sem todos os campos obrigatórios "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

    def test_song_creation_without_token(self):
        response = self.client.post(self.BASE_URL, data={}, format="json")

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se a mensagem de retorno do POST sem token"
            + f"em `{self.BASE_URL}` está correta."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

        # STATUS CODE
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

    def test_song_creation_with_valid_token(self):
        song_data = {"title": "Unreachable", "duration": "130"}

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        response = self.client.post(self.BASE_URL, data=song_data, format="json")

        # RETORNO JSON
        expected_data = {"id": 1, "album_id": self.album.pk, **song_data}
        resulted_data = response.json()
        msg = (
            "Verifique se as informações retornadas no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

        # STATUS CODE
        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)
