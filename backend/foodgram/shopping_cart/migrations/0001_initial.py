# Generated by Django 4.1.7 on 2023-04-04 04:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe', '0002_remove_recipe_is_in_shopping_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='InShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe_in_cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_in_cart', to='recipe.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopper', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
