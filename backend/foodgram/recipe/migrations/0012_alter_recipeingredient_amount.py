# Generated by Django 4.1.7 on 2023-02-24 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0011_recipeingredient_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
