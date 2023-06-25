from api.tests.constants import Constants as c
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user
from django.test import Client, TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token

from ingredients.models import Ingredient
from recipe.models import Recipe, RecipeIngredient
from tags.models import Tag
from api.views import FavoritedCreateDeleteViewSet

User = get_user_model()


class RecipeApiTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        factory = APIRequestFactory()
        cls.authorized_user1 = User.objects.create(
            username=c.USERNAME1,
            role='user',
            first_name='user_first',
            last_name='user_last',
            email='user1@user.com'
        )
        cls.authorized_client1 = Client()
        cls.authorized_client1.force_login(cls.authorized_user1)

        cls.authorized_user2 = User.objects.create(
            username='username_authorized2',
            role='user2',
            first_name='user_first2',
            last_name='user_last2',
            email='user2@user.com'
        )
        cls.authorized_client2 = Client()
        cls.authorized_client2.force_login(cls.authorized_user2)

        cls.factory = APIRequestFactory()
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

    def test_recipe_created(self):
        # сначала разобраться с логином/получением токена
        pass

        # self.assertEqual(2, 2)
