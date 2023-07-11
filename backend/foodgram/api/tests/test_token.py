import logging

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.test import TestCase

logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)


User = get_user_model()

USER2_USERNAME = 'username_authorized2'
USER2_EMAIL = 'user2@user.com'


class RecipeApiTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_getting_token(self):
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

        response = self.client.post('/api/auth/token/login/',
                                    {"password": "Qwerty123",
                                     "email": "vpupkin@yandex.ru",
                                     },
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
