from api.tests.constants import Constants as c
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user
from django.test import Client, TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
import logging

from ingredients.models import Ingredient
from recipe.models import Recipe, RecipeIngredient
from tags.models import Tag
from api.views import FavoritedCreateDeleteViewSet

User = get_user_model()
logger = logging.getLogger(__name__)
log = logging.getLogger(__name__)


class RecipeApiTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        # cls.guest_client = Client()
        # factory = APIRequestFactory()
        # cls.authorized_user1 = User.objects.create(
        #     username=c.USERNAME1,
        #     role='user',
        #     first_name='user_first',
        #     last_name='user_last',
        #     email='user1@user.com'
        # )
        # cls.authorized_client1 = Client()
        # cls.authorized_client1.force_login(cls.authorized_user1)

        # cls.authorized_user2 = User.objects.create(
        #     username='username_authorized2',
        #     role='user2',
        #     first_name='user_first2',
        #     last_name='user_last2',
        #     email='user2@user.com'
        # )
        # cls.authorized_client2 = Client()
        # cls.authorized_client2.force_login(cls.authorized_user2)

        # cls.factory = APIRequestFactory()
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

    def setUp(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_recipe_created(self):
        """Creates a user and a test reipe via API"""

        self.assertEqual(Recipe.objects.count(), 0,
                         'no legacy recipes confirmed')

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
        if response_login.data:
            log.info(f'response login data {response_login.data}')

        # self.assertEqual(response_login.status_code, 201) # таргет
        self.assertEqual(response_login.status_code, 200)

        token = Token.objects.get(user=user)
        log.info(f'Token {token}')
        self.client.force_login(user)

        response_post = self.client.post(
            '/api/recipes/', {
                "ingredients": [
                    {"id": f'{self.ingredient1.id}', "amount": 10}
                ],
                "tags": [self.tag1.id, self.tag2.id],
                "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
                "name": "string",
                "text": "string",
                "cooking_time": 1
            },
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Token {token}"},
            # follow=True
        )

        # Make sure that the authorization works properly

        # log.info(f'response login data {response_post}')
        # log.info(f'response login data {response_post}')
        # log.info(f'response login data {dir(response_post)}')
        # log.info(f'response response_post.content {response_post.content}')
        # log.info(f'response response_post.content {print(response_post)}')
        # log.info(f'response response_post.content {response_post.url}')
        log.info(response_post.status_code)
        # log.info(f'redirect chain: {response_post.redirect_chain}')
        # self.assertEqual(response_post.status_code, 201)
        self.assertEqual(Recipe.objects.count(), 1)
