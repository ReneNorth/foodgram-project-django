from api.tests.constants import Constants as c
from django.contrib.auth import get_user_model, get_user
from django.test import Client, TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
import logging

from ingredients.models import Ingredient
from recipe.models import Recipe
from tags.models import Tag

User = get_user_model()
logger = logging.getLogger(__name__)
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
        cls.authorized_user2 = User.objects.create(
            username=c.USER2_USERNAME,
            role='user2',
            first_name='user_first2',
            last_name='user_last2',
            email='user2@user.com',
            password='12345'
        )

        cls.recipe1 = Recipe.objects.create(
            author=cls.authorized_user2,
            name=c.RECIPE1_NAME,
            text='test text1',
            cooking_time=10,
        )
        cls.recipe1.tags.set(
            [Tag.objects.get(name=c.TAG1_NAME).id])
        cls.recipe1.ingredients.set(
            [Ingredient.objects.get(name='test_ingredient1').id])

    def setUp(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_recipe_created(self):
        """Creates a user and a test reipe via API"""

        # self.assertEqual(Recipe.objects.count(), 0,
        #                  'no legacy recipes confirmed')

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

        token = Token.objects.get(user=user)
        self.client.force_login(user)

        tag1_id = Tag.objects.get(name=c.TAG1_NAME).id
        tag2_id = Tag.objects.get(name=c.TAG2_NAME).id

        response_post = self.client.post(
            '/api/recipes/', {
                "ingredients": [
                    {"id": f'{self.ingredient1.id}', "amount": 10}
                ],
                "tags": [tag1_id, tag2_id],
                "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
                "name": "string_rec",
                "text": "string",
                "cooking_time": 1
            },
            content_type="application/json",
            **{"HTTP_AUTHORIZATION": f"Token {token}"},
        )
        log.info(response_post.request)
        log.info(response_post.content)
        log.info(response_post.context)
        log.info(response_post.status_text)
        log.info(dir(response_post))
        self.assertEqual(response_post.status_code, 201)
        recipe = get_object_or_404(Recipe, name='string_rec')
        self.assertEqual(recipe.name, 'string_rec')
        self.assertEqual(recipe.text, 'string')

    def test_ingredients_returned(self):
        recipe = get_object_or_404(Recipe, name=c.RECIPE1_NAME)
        log.info(f'fpund recipe:{recipe}')
        response = self.client.get(f'/api/recipes/{recipe.id}/')
        self.assertEqual(response.status_code, 200)
        log.info(response)

        ingredients = response.data['ingredients'][0]
        log.info(ingredients)
        log.info(len(ingredients))
        self.assertGreater(len(ingredients), 0)
        # self.assertIsInstance(ingredients, list)
