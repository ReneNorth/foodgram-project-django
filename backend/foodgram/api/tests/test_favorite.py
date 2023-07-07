import logging

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.test import TestCase

from api.tests.constants import Constants as c
from ingredients.models import Ingredient
from recipe.models import Recipe
from tags.models import Tag

logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)


User = get_user_model()

USER2_USERNAME = 'username_authorized2'
USER2_EMAIL = 'user2@user.com'


class RecipeApiTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.authorized_user1 = User.objects.create(
            username='username_authorized',
            role='user',
            first_name='user_first',
            last_name='user_last',
            email='user1@user.com',
            password='12345'
        )
        cls.authorized_user2 = User.objects.create(
            username=USER2_USERNAME,
            role='user2',
            first_name='user_first2',
            last_name='user_last2',
            email='user2@user.com',
            password='12345'
        )
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

        cls.recipe1 = Recipe.objects.create(
            author=cls.authorized_user1,
            name=c.RECIPE1_NAME,
            text='test text1',
            cooking_time=10,
        )
        cls.recipe1.tags.set(
            [Tag.objects.get(name=c.TAG1_NAME).id])
        cls.recipe1.ingredients.set(
            [Ingredient.objects.get(name='test_ingredient1').id])

        cls.recipe2 = Recipe.objects.create(
            author=cls.authorized_user1,
            name=c.RECIPE2_NAME,
            text='test text2',
            cooking_time=10,
        )
        cls.recipe2.tags.set(
            [Tag.objects.get(name=c.TAG2_NAME).id])
        cls.recipe2.ingredients.set(
            [Ingredient.objects.get(name='test_ingredient2').id])

    def setUp(self) -> None:
        pass

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
