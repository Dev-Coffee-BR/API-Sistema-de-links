import datetime
from urllib import request
from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate

from user.models import User

from user.views import (
    Register,
    DeleteUser,
    PutUser,
    ChangePassword,
    CountUsers,
    UserViewSet,
)

# Create your tests here.


class CreateUserTest(TestCase):
    def setUp(self):
        User.objects.create(
            email="abc@teste.com", password="123", first_name="João", last_name="Silva"
        )

    def test_create_user(self):
        user = User.objects.get(email="abc@teste.com")

        self.assertFalse(user.soft_delet)
        self.assertTrue(user.is_active)
        self.assertEqual(user.first_name, "João")
        self.assertEqual(user.last_name, "Silva")


class SoftDeleteUserTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            email="abcd@teste.com", password="123", first_name="João", last_name="Silva"
        )
        user.soft_delete()

    def test_soft_delete_user(self):
        user = User.objects.get(email="abcd@teste.com")

        self.assertTrue(user.soft_delet)
        self.assertFalse(user.is_active)
        self.assertEqual(user.first_name, "João")
        self.assertEqual(user.last_name, "Silva")


class ResgisterUserTest(TestCase):
    def setUp(self):
        ...

    def test_register_user(self):
        factory = APIRequestFactory()
        data = {
            "email": "teste@teste.com",
            "password": "123",
            "first_name": "João",
            "last_name": "Silva",
        }

        request = factory.post("/api/user/register/", data, format="json")

        response = Register.as_view()(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["success"], True)


class RegisterUserFailTest(TestCase):
    def setUp(self):
        User.objects.create(
            email="teste@teste.com",
            password="123",
            first_name="João",
            last_name="Silva",
        )

    def test_register_user_fail(self):
        factory = APIRequestFactory()
        data = {
            "email": "teste@teste.com",
            "password": "123",
            "first_name": "João",
            "last_name": "Silva",
        }

        request = factory.post("/api/user/register/", data, format="json")

        response = Register.as_view()(request)

        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data["success"], False)


class ResgisterUserEmptyFieldTest(TestCase):
    def setUp(self):
        ...

    def test_register_empty_field_user(self):
        factory = APIRequestFactory()
        data = {
            "email": "teste@teste.com",
        }

        request = factory.post("/api/user/register/", data, format="json")

        response = Register.as_view()(request)

        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.data["success"], False)


class RegisterDeletedUserTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            email="teste@teste.com",
            password="123",
            first_name="João",
            last_name="Silva",
        )

        user.soft_delete()

    def test_register_deleted_user(self):
        factory = APIRequestFactory()
        data = {
            "email": "teste@teste.com",
            "password": "123",
            "first_name": "João",
            "last_name": "Carlos",
        }

        request = factory.post("/api/user/register/", data, format="json")

        response = Register.as_view()(request)

        user = User.objects.get(email="teste@teste.com")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(user.last_name, "Carlos")


class CountUserTest(TestCase):
    def setUp(self):
        User.objects.create(
            email="teste@teste.com",
            password="123",
            first_name="João",
            last_name="Silva",
        )

    def test_count_user(self):
        factory = APIRequestFactory()
        request = factory.get("/api/user/count/users/")

        response = CountUsers.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(response.data["num_users"], 1)


class DeleteUserTest(TestCase):
    def setUp(self):
        User.objects.create(
            email="teste@teste.com",
            password="123",
            first_name="João",
            last_name="Silva",
        )

    def test_delete_user(self):
        factory = APIRequestFactory()
        request = factory.delete("/api/user/delete/")

        user = User.objects.get(email="teste@teste.com")

        force_authenticate(request, user)

        response = DeleteUser.as_view()(request)

        user = User.objects.get(email="teste@teste.com")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)
        self.assertTrue(user.soft_delet)


class DeleteUserFailTest(TestCase):
    def setUp(self):
        User.objects.create(
            email="teste@teste.com",
            password="123",
            first_name="João",
            last_name="Silva",
        )

    def test_delete_user(self):
        factory = APIRequestFactory()
        request = factory.delete("/api/user/delete/")

        response = DeleteUser.as_view()(request)

        user = User.objects.get(email="teste@teste.com")

        self.assertEqual(response.status_code, 401)
        self.assertFalse(user.soft_delet)


class PutUserTest(TestCase):
    def setUp(self):
        User.objects.create(
            email="teste@teste.com",
            password="123",
            first_name="João",
            last_name="Silva",
        )

    def test_put_user(self):
        factory = APIRequestFactory()

        data = {
            "email": "teste2@teste.com",
            "first_name": "Paulo",
            "last_name": "Silva",
        }

        request = factory.put("/api/user/alter/user/", data, format="json")

        user = User.objects.get(email="teste@teste.com")

        force_authenticate(request, user)

        response = PutUser.as_view()(request)

        user = User.objects.all().filter(email="teste@teste.com").first()
        user2 = User.objects.get(email="teste2@teste.com")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success"], True)
        self.assertFalse(user)
        self.assertTrue(user2)


class ChangePasswordTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            email="teste@teste.com", first_name="João", last_name="Silva"
        )
        user.set_password("123")
        user.save()

    def test_change_password(self):
        factory = APIRequestFactory()

        data = {
            "password": "123",
            "new_password": "456",
        }

        request = factory.post("/api/user/change/password/", data, format="json")

        user = User.objects.get(email="teste@teste.com")

        force_authenticate(request, user)

        response = ChangePassword.as_view()(request)

        user = User.objects.get(email="teste@teste.com")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.check_password("456"))
        self.assertFalse(user.check_password("123"))


class ChangePasswordFailTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            email="teste@teste.com", first_name="João", last_name="Silva"
        )
        user.set_password("123")
        user.save()

    def test_change_password(self):
        factory = APIRequestFactory()

        data = {
            "password": "124",
            "new_password": "456",
        }

        request = factory.post("/api/user/change/password/", data, format="json")

        user = User.objects.get(email="teste@teste.com")

        force_authenticate(request, user)

        response = ChangePassword.as_view()(request)

        user = User.objects.get(email="teste@teste.com")

        self.assertEqual(response.status_code, 401)
        self.assertFalse(user.check_password("456"))
        self.assertTrue(user.check_password("123"))
