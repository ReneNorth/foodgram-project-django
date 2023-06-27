from api.tests.constants import Constants as c
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user
from django.test import Client, TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token
import logging

from ingredients.models import Ingredient
from recipe.models import Recipe, RecipeIngredient
from tags.models import Tag
from api.views import FavoritedCreateDeleteViewSet

User = get_user_model()

logger = logging.getLogger(__name__)
log = logging.getLogger(__name__)


# вынести в constants
TAG1_NAME = 'test_tag1'
TAG2_NAME = 'test_tag2'
RECIPE1_NAME = 'test_recipe1'
RECIPE2_NAME = 'test_recipe2'
TAG1_SLUG = 'black'
TAG2_SLUG = 'green'


class RecipeApiTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        factory = APIRequestFactory()
        cls.authorized_user1 = User.objects.create(
            username='username_authorized',
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
            name=TAG1_NAME,
            color='black',
            slug=TAG1_SLUG
        )
        cls.tag2 = Tag.objects.create(
            name=TAG2_NAME,
            color='green',
            slug=TAG2_SLUG
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
            name=RECIPE1_NAME,
            text='test text1',
            cooking_time=10,
        )
        cls.recipe1.tags.set(
            [Tag.objects.get(name=TAG1_NAME).id])
        cls.recipe1.ingredients.set(
            [Ingredient.objects.get(name='test_ingredient1').id])

        cls.recipe2 = Recipe.objects.create(
            author=cls.authorized_user1,
            name=RECIPE2_NAME,
            text='test text2',
            cooking_time=10,
        )
        cls.recipe2.tags.set(
            [Tag.objects.get(name=TAG2_NAME).id])
        cls.recipe2.ingredients.set(
            [Ingredient.objects.get(name='test_ingredient2').id])

    def setUp(self) -> None:
        pass

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_recipe_created(self):
        self.assertEqual(Recipe.objects.count(), 2)

    def test_recipe_list(self):
        response = self.guest_client.get('/api/recipes/',
                                         content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_recipe_get(self):
        """Test getting a recipe by ID."""
        recipe_id = Recipe.objects.get(name=RECIPE1_NAME).id
        response = self.guest_client.get(
            f'/api/recipes/{recipe_id}/',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_recipe_filter_tag(self):
        """
        Checks that 2 tags are created but a query with one tag
        returns only one recipe.
        """
        self.assertAlmostEqual(Tag.objects.count(), 2)
        response = self.guest_client.get(
            f'/api/recipes/?page=1&limit=6&tags={TAG1_SLUG}',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)

    def test_recipe_filter_2_tags(self):
        """Checks that a query with two tags returns 2 elements"""
        log.info(f'no of recipes in the database: {Recipe.objects.count()}')
        response = self.guest_client.get(
            f'/api/recipes/?page=1&limit=6&tags={TAG1_SLUG}&tags={TAG2_SLUG}',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 2)

    def user_crerated(self):
        self.assertAlmostEqual(User.objects.count(), 2)
