import logging

from api.tests.constants import Constants as c
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase
from ingredients.models import Ingredient
from rest_framework.authtoken.models import Token
from tags.models import Tag

User = get_user_model()
log = logging.getLogger(__name__)


class RecipeApiTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

        cls.tag1 = Tag.objects.create(
            name=c.TAG1_NAME,
            color='black',
            slug=c.TAG1_SLUG
        )
        cls.tag2 = Tag.objects.create(
            name=c.TAG2_NAME,
            color='green',
            slug=c.TAG2_SLUG
        )
        cls.ingredient1 = Ingredient.objects.create(
            name='test_ingredient1',
            measurement_unit='kg'
        )
        cls.ingredient2 = Ingredient.objects.create(
            name='test_ingredient2',
            measurement_unit='kg'
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_user_url_available(self):
        """Creates a user and a test reipe via API"""

        response_create_user = self.client.post('/api/users/',
                                                {"email": "vpupkin@yandex.ru",
                                                 "username": "vasya.pupkin",
                                                 "first_name": "Вася",
                                                 "last_name": "Пупкин",
                                                 "password": "Qwerty123", },
                                                'application/json')
        self.assertEqual(response_create_user.status_code, 201)
        user = get_object_or_404(User, email='vpupkin@yandex.ru')
        response_login = self.client.post('/api/auth/token/login/',
                                          {
                                              "password": "Qwerty123",
                                              "email": "vpupkin@yandex.ru"
                                          },
                                          "application/json")

        # self.assertEqual(response_login.status_code, 201) # таргет
        self.assertEqual(response_login.status_code, 200)
        self.client.force_login(user)

        response_user_page = self.client.get(
            f'/api/users/{user.id}/',
            # **{"HTTP_AUTHORIZATION": f"Token {token}"}
        )
        self.assertEqual(response_user_page.status_code, 200)

    def test_user_me_available(self):
        response_create_user = self.client.post('/api/users/',
                                                {"email": "vpupkin@yandex.ru",
                                                 "username": "vasya.pupkin",
                                                 "first_name": "Вася",
                                                 "last_name": "Пупкин",
                                                 "password": "Qwerty123", },
                                                'application/json')
        self.assertEqual(response_create_user.status_code, 201)
        user = get_object_or_404(User, email='vpupkin@yandex.ru')
        self.assertEqual(user.email, 'vpupkin@yandex.ru')

        response_login = self.client.post('/api/auth/token/login/',
                                          {
                                              "password": "Qwerty123",
                                              "email": "vpupkin@yandex.ru"
                                          },
                                          "application/json")

        # self.assertEqual(response_login.status_code, 201) # таргет
        self.assertEqual(response_login.status_code, 200)

        token = Token.objects.get(user=user)
        self.client.force_login(user)

        response_me = self.client.get(
            '/api/users/me/',
            **{"HTTP_AUTHORIZATION": f"Token {token}"},
        )
        self.assertEqual(response_me.status_code, 200)

        response_subscriptions = self.client.get(
            '/api/users/subscriptions/',
            **{"HTTP_AUTHORIZATION": f"Token {token}"},
        )
        self.assertEqual(response_subscriptions.status_code, 200)
