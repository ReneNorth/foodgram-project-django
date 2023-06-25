
from api.tests.constants import Constants as c
import json
import logging
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
from rest_framework.authtoken.models import Token

from rest_framework.test import RequestsClient
from ingredients.models import Ingredient
from recipe.models import Recipe, RecipeIngredient
from tags.models import Tag
from api.views import FavoritedCreateDeleteViewSet

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
        # user = get_object_or_404(User, email='user2@user.com')
        # client = RequestsClient()

        # response_get = self.client.get('/api/recipes/')
        # self.assertEqual(response_get.status_code, 200)

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

        response_post = self.client.post(
            '/api/recipes', {
                "ingredients": [
                    {"id": 1123, "amount": 10}
                ],
                "tags": [1, 2],
                "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
                "name": "string",
                "text": "string",
                "cooking_time": 1
            },
            content_type="application/json",
        )
        # self.assertEqual(response_post.status_code, 200, response_post.data)

    def test_favorite(self):
        """Unfinished"""

        # view = FavoritedCreateDeleteViewSet.as_view({'post': 'create'})
        # recipe_id = Recipe.objects.get(name=RECIPE1_NAME).id
        # print(recipe_id)
        # print(self.authorized_user2)
        # request = self.factory.post('/api/recipes/1/favorite/')
        # force_authenticate(request, user=self.authorized_user2,
        #                    )
        # response = view(request)

        # print(response.status_code, 201)
        # self.assertEqual(response.status_code, 201)

        # view = FavoritedCreateDeleteViewSet.as_view({'post': 'create'})
        # recipe_id = Recipe.objects.get(name=RECIPE1_NAME).id
        # print(recipe_id)
        # print(self.authorized_user2)
        # request = self.factory.post('/api/recipes/1/favorite/')
        # force_authenticate(request, user=self.authorized_user2,
        #                    token=self.authorized_user2.auth)
        # response = view(request)

        # print(response.status_code, 201)
        # self.assertEqual(response.status_code, 201)
        # recipe_id = Recipe.objects.get(name=RECIPE1_NAME).id
        # self.authorized_client2.force_login(user=self.authorized_user2)
        # self.client.login(username='fred', password='secret')
        # print(get_user(self.authorized_client2).is_authenticated)
        # self.assertTrue(get_user(self.authorized_client2).is_authenticated)

        # token = Token.objects.get(
        #     user=self.authorized_user2)
        # print(token)
        # self.authorized_client2.credentials(
        #     HTTP_AUTHORIZATION='Token ' + token.key)

        # response = self.authorized_client2.post(
        #     f'/api/recipes/{recipe_id}/favorite/',
        #     content_type='application/json',
        # )
        # print(dir(response))
        # print(response.status_text)
        # self.assertEqual(response.status_code, 201)

        # response = self.authorized_client2.delete(
        #     f'/api/recipes/{recipe_id}/favorite/',
        #     content_type='application/json')
        # self.assertEqual(response.status_code, 204)
