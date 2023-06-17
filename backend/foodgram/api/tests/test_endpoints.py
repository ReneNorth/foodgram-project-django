from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from rest_framework.test import APIRequestFactory

from ingredients.models import Ingredient
from recipe.models import Recipe, RecipeIngredient
from tags.models import Tag

User = get_user_model()


class RecipeApiTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create(

        )
        cls.factory = APIRequestFactory()
        cls.tag = Tag.objects.create(
            name='test_tag',
            color='black',
            slug='black'
        )
        cls.ingredient = Ingredient.objects.create(
            name='test_ingredient',
            measurement_unit='kg'
        )

        cls.recipe = Recipe.objects.create(
            author=cls.user,
            name='test_recipe',
            text='test text',
            cooking_time=10,
        )
        cls.recipe.tags.set(
            [Tag.objects.get(name='test_tag').id])
        cls.recipe.ingredients.set(
            [Ingredient.objects.get(name='test_ingredient').id])

    def setUp(self) -> None:
        pass

    def test_recipe_created(self):
        self.assertEqual(Recipe.objects.count(), 1)

    def test_recipe_list(self):
        response = self.guest_client.get('/api/recipes/',
                                         content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_recipe_get(self):
        """Test getting a recipe by ID."""
        recipe_id = Recipe.objects.get(name="test_recipe").id
        response = self.guest_client.get(
            f'/api/recipes/{recipe_id}/',
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
