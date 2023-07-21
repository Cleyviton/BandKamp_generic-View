from rest_framework.test import APITestCase
from rest_framework.views import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


User: AbstractUser = get_user_model()


class UserRegistrationViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.BASE_URL = "/api/users/"

        # UnitTest Longer Logs
        cls.maxDiff = None

    def test_user_creation_without_required_fields(self):
        response = self.client.post(self.BASE_URL, data={}, format="json")

        # RETORNO JSON
        resulted_data: dict = response.json()
        expected_fields = {
            "email",
            "username",
            "password",
            "artistic_name",
        }
        returned_fields = set(resulted_data.keys())

        msg = "Verifique se todas as chaves obrigatórias são retornadas ao tentar criar um usuário sem dados"
        self.assertSetEqual(expected_fields, returned_fields, msg)

        # STATUS CODE
        expected_status_code = status.HTTP_400_BAD_REQUEST
        resulted_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST sem todos os campos obrigatórios "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, resulted_status_code, msg)

    def test_user_creation(self):
        user_data = {
            "username": "lucira_buster",
            "email": "lucira_buster@kenziebuster.com",
            "full_name": "Lucira",
            "artistic_name": "Buster",
            "password": "1234",
        }

        response = self.client.post(self.BASE_URL, data=user_data, format="json")

        added_user = User.objects.last()
        # RETORNO JSON
        expected_data = {
            "id": added_user.pk,
            "username": "lucira_buster",
            "email": "lucira_buster@kenziebuster.com",
            "full_name": "Lucira",
            "artistic_name": "Buster",
        }
        resulted_data = response.json()
        msg = (
            "Verifique se as informações do usuário retornada no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertDictEqual(expected_data, resulted_data, msg)

        # PASSWORD HASHEADO
        msg = "Verifique se o password foi hasheado corretamente"
        self.assertTrue(added_user.check_password(user_data["password"]), msg)

        # STATUS CODE
        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)

    def test_non_unique_username_or_email_user_creation(self):
        user_data = {
            "username": "lucira",
            "email": "lucira@mail.com",
            "full_name": "Lucira",
            "artistic_name": "Buster",
            "password": "1234",
        }
        # Populando o banco pré testagem
        User.objects.create_superuser(**user_data)
        response = self.client.post(self.BASE_URL, data=user_data, format="json")

        # RETORNO JSON
        resulted_data = response.json()
        expected_fields = {"username", "email"}
        resulted_fields = set(resulted_data.keys())
        msg = (
            "Verifique se as informações do usuário retornada no POST "
            + f"em `{self.BASE_URL}` estão corretas."
        )
        self.assertSetEqual(expected_fields, resulted_fields, msg)

        # ERROR MESSAGES
        resulted_username_message = resulted_data["username"][0]
        resulted_email_message = resulted_data["email"][0]

        expected_username_message = "A user with that username already exists."
        expected_email_message = "This field must be unique."

        msg = (
            "Verifique a mensagem de erro quando criando usuário com username repetido"
        )
        self.assertEqual(expected_username_message, resulted_username_message, msg)

        msg = "Verifique a mensagem de erro quando criando usuário com email repetido"
        self.assertEqual(expected_email_message, resulted_email_message, msg)

        # STATUS CODE
        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code
        msg = (
            "Verifique se o status code retornado do POST "
            + f"em `{self.BASE_URL}` é {expected_status_code}"
        )
        self.assertEqual(expected_status_code, result_status_code, msg)
