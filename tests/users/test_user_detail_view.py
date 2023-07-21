from rest_framework.test import APITestCase
from rest_framework.views import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from tests.factories import create_user_with_token


User: AbstractUser = get_user_model()


class UserDetailViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1, token_1 = create_user_with_token()
        cls.access_token_1 = str(token_1.access_token)
        user_2_data = {
            "username": "lucira_buster_2",
            "email": "lucira_buster_2@kenziebuster.com",
            "full_name": "Lucira",
            "artistic_name": "Buster",
            "password": "1234",
        }

        cls.user_2, token_2 = create_user_with_token(user_data=user_2_data)
        cls.access_token_2 = str(token_2.access_token)

        cls.BASE_URL = f"/api/users/{cls.user_1.id}/"

        # UnitTest Longer Logs
        cls.maxDiff = None

    def test_retrieve_user_without_token(self):
        response = self.client.get(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET sem token "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {
            "id": self.user_1.pk,
            "username": self.user_1.username,
            "email": self.user_1.email,
            "full_name": self.user_1.full_name,
            "artistic_name": self.user_1.artistic_name,
        }
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do GET com token correto em "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_retrieve_user_with_correct_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.get(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do GET com token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {
            "id": self.user_1.pk,
            "username": self.user_1.username,
            "email": self.user_1.email,
            "full_name": self.user_1.full_name,
            "artistic_name": self.user_1.artistic_name,
        }
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do GET com token correto em "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_delete_user_without_token(self):
        response = self.client.delete(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE sem token "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do DELETE sem token "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_delete_user_with_another_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.delete(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE sem token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        expected_message = {
            "detail": "You do not have permission to perform this action."
        }
        resulted_message = response.json()
        msg = f"Verifique se a mensagem retornada do DELETE em {self.BASE_URL} está correta"
        self.assertDictEqual(expected_message, resulted_message, msg)

    def test_delete_user_with_correct_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.delete(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_204_NO_CONTENT
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do DELETE com token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

    def test_update_user_without_token(self):
        response = self.client.patch(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_401_UNAUTHORIZED
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH sem token "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {"detail": "Authentication credentials were not provided."}
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH sem token "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

    def test_update_user_with_another_user_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_2)
        response = self.client.patch(self.BASE_URL, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_403_FORBIDDEN
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH sem token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        expected_message = {
            "detail": "You do not have permission to perform this action."
        }
        resulted_message = response.json()
        msg = f"Verifique se a mensagem retornada do PATCH em {self.BASE_URL} está correta"
        self.assertDictEqual(expected_message, resulted_message, msg)

    def test_update_user_with_correct_user_token(self):
        info_to_patch = {
            "username": "lucira_buster_5000",
            "email": "lucira_buster_5000@kenziebuster.com",
            "full_name": "Lucira5000",
            "artistic_name": "Buster5000",
            "password": "lucira1234!@@@3",
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_1)
        response = self.client.patch(self.BASE_URL, data=info_to_patch, format="json")

        # STATUS CODE
        expected_status_code = status.HTTP_200_OK
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do PATCH com token correto "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

        # RETORNO JSON
        expected_data = {
            "id": self.user_1.pk,
            "username": info_to_patch["username"],
            "email": info_to_patch["email"],
            "full_name": info_to_patch["full_name"],
            "artistic_name": info_to_patch["artistic_name"],
        }
        resulted_data = response.json()
        msg = (
            "Verifique se os dados retornados do PATCH com token correto em "
            + f"em `{self.BASE_URL}` é {expected_data}"
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

        user = User.objects.first()
        msg = (
            f"Verifique se a senha está sendo atualizada no {response.request['REQUEST_METHOD']} em "
            + f"em `{self.BASE_URL}`"
        )
        import ipdb

        # ipdb.set_trace()
        self.assertTrue(user.check_password(info_to_patch["password"]), msg)
