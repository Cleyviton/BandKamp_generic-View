from rest_framework.test import APITestCase
from rest_framework.views import status
from tests.factories import create_user_with_token, create_multiple_albums_with_user
import ipdb


class AlbumViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/albums/"

        # UnitTest Longer Logs
        cls.maxDiff = None

    def test_albums_listing_pagination(self):
        user, token = create_user_with_token()
        albums_count = 10
        create_multiple_albums_with_user(user, albums_count)

        response = self.client.get(self.BASE_URL)
        resulted_data = response.json()
        resulted_pagination_keys = set(resulted_data.keys())
        expected_pagination_keys = {"count", "next", "previous", "results"}
        msg = "Verifique se a paginação está sendo feita corretamente"
        with self.subTest():
            self.assertSetEqual(expected_pagination_keys, resulted_pagination_keys)

        results_len = len(resulted_data["results"])
        expected_len = 2
        msg = "Verifique se a paginação está retornando apenas dois items de cada vez"
        self.assertEqual(expected_len, results_len, msg)

    def test_album_creation_without_required_fields(self):
        _, token = create_user_with_token()
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(token.access_token))
        response = self.client.post(self.BASE_URL, data={}, format="json")

        # STATUS CODE
        with self.subTest():
            expected_status_code = status.HTTP_400_BAD_REQUEST
            resulted_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST sem todos os campos obrigatórios "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        resulted_data: dict = response.json()
        expected_fields = {
            "name",
            "year",
        }
        returned_fields = set(resulted_data.keys())
        msg = "Verifique se todas as chaves obrigatórias são retornadas ao tentar criar uma música sem dados"
        self.assertSetEqual(expected_fields, returned_fields, msg)

    def test_album_creation_without_token(self):
        # STATUS CODE
        with self.subTest():
            response = self.client.post(self.BASE_URL, data={}, format="json")
            expected_status_code = status.HTTP_401_UNAUTHORIZED
            result_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )

            self.assertEqual(expected_status_code, result_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se a mensagem de retorno do POST sem token"
            + f"em `{self.BASE_URL}` está correta."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_album_creation_with_valid_token(self):
        album_data = {
            "name": "Shadows Collide with People",
            "year": 200,
        }

        # STATUS CODE
        with self.subTest():
            user_data, token = create_user_with_token()
            self.client.credentials(
                HTTP_AUTHORIZATION="Bearer " + str(token.access_token)
            )
            response = self.client.post(self.BASE_URL, data=album_data, format="json")
            expected_status_code = status.HTTP_201_CREATED
            result_status_code = response.status_code
            msg = (
                "Verifique se o status code retornado do POST "
                + f"em `{self.BASE_URL}` é {expected_status_code}"
            )
            self.assertEqual(expected_status_code, result_status_code, msg)

        # RETORNO JSON
        user_detail = {
            "artistic_name": user_data.artistic_name,
            "email": user_data.email,
            "full_name": user_data.full_name,
            "id": user_data.pk,
            "username": user_data.username,
        }
        expected_data = {"id": 1, "user": user_detail, **album_data}
        resulted_data = response.json()
        msg = (
            "Verifique se as informações retornadas no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)
