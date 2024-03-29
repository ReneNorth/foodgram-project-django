# Generated by Django 4.1.7 on 2023-06-17 16:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ingredients", "0003_remove_ingredient_amount"),
        ("recipe", "0003_alter_recipetag_tag"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="ingredients",
            field=models.ManyToManyField(
                through="recipe.RecipeIngredient", to="ingredients.ingredient"
            ),
        ),
        migrations.AlterField(
            model_name="recipeingredient",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ingredients_in_recipe",
                to="recipe.recipe",
            ),
        ),
    ]
